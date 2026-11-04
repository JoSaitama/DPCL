"""Offline, single-seed noise/beta comparisons; no training framework is imported.

Repeat --adam-dir/--flip-dir/--filter-dir for explicit runs. Each noise cohort
needs one Adam and matching Flip/Filter beta sets. See --help for controls.
"""

import argparse
from collections import defaultdict, deque
import csv
from dataclasses import dataclass
from datetime import datetime
import hashlib
from io import StringIO
import json
import math
from pathlib import Path
import re


ROOT = Path(__file__).resolve().parents[1]
STYLES = {
    "adam": ("Adam", "#1f77b4", "-"),
    "flip": ("DPCL Flip", "#d62728", "-"),
    "filter": ("DPCL Filter", "#ff7f0e", "--"),
}
PLOTS = ("noise-accuracy", "tradeoff", "test-accuracy", "edit-rate")
MARKERS = ("o", "s", "^", "D", "v", "P", "X")
GROUPS = {"clean": "original", "corrupted_original": "original",
          "corrupted_noisy": "reference"}


def numeric(row, key, source, *, integer=False, minimum=0, maximum=math.inf):
    try:
        value = float(row[key])
        if not math.isfinite(value) or not minimum <= value <= maximum:
            raise ValueError()
        if integer and not value.is_integer():
            raise ValueError()
    except (KeyError, TypeError, ValueError):
        raise ValueError(f"{source}: invalid {key}={row.get(key)!r}") from None
    return int(value) if integer else value


def read_bytes(path, sources):
    data = path.read_bytes()
    sources[path] = hashlib.sha256(data).hexdigest()
    return data


def rows(path, required, sources):
    reader = csv.DictReader(StringIO(read_bytes(path, sources).decode("utf-8-sig")))
    if not required <= set(reader.fieldnames or ()):
        raise ValueError(f"{path}: missing columns {sorted(required - set(reader.fieldnames or ()))}")
    found = False
    for row in reader:
        found = True
        yield row
    if not found:
        raise ValueError(f"{path}: empty CSV")


def resolve_input(value):
    path = Path(value).expanduser()
    if not path.is_absolute():
        path = ROOT / "results/files" / path if len(path.parts) == 1 else ROOT / path
    return path.resolve()


@dataclass
class Run:
    method: str
    directory: Path
    beta: float | None
    seed: int
    counts: tuple
    points: list
    edits: list
    sources: dict
    metadata: dict | None

    @property
    def noise_percent(self):
        return 100 * self.counts[1] / sum(self.counts)


def identity(method, directory, sources):
    """Use metadata if exported, otherwise explicit run-name identities."""
    metadata = None
    for parent in directory.parents:
        if parent.name == "files":
            path = parent.parent / "logs" / directory.name / "metadata.json"
            if path.is_file():
                metadata = json.loads(read_bytes(path, sources))
            break
    seed_match = re.search(r"(?:^|_)adam_(\d+)(?:_|$)", directory.name)
    beta_match = re.search(r"_ema_b([0-9.]+)_", directory.name)
    weight_match = re.search(r"_w(-?[0-9.]+)_", directory.name)
    if method == "adam" and any(token in directory.name for token in ("_dpcl_", "_dpco_")):
        raise ValueError(f"{directory}: DPCL run cannot be labelled as the Adam baseline")
    if method != "adam":
        expected_weight = -1 if method == "flip" else 0
        if weight_match and float(weight_match[1]) != expected_weight:
            raise ValueError(f"{directory}: filename weight does not match {method}")
        if metadata is None and not weight_match:
            raise ValueError(f"{directory}: intervention identity missing; export metadata or retain the original run name")
    seed = int(seed_match[1]) if seed_match else None
    beta = float(beta_match[1]) if beta_match and method != "adam" else None
    if metadata is not None:
        config = metadata["config"]
        expected = ("adam",) if method == "adam" else ("dpcl", "dpco")
        if config["training"].get("optimizer", "sgd") != "adam" or config["method"]["name"] not in expected:
            raise ValueError(f"{directory}: metadata does not describe {method} + Adam")
        actual_seed = int(config["seed"])
        if seed is not None and actual_seed != seed:
            raise ValueError(f"{directory}: filename and metadata seeds disagree")
        seed = actual_seed
        if method != "adam":
            reference = config["reference"]
            actual_beta = float(reference["beta"])
            weight = config["method"].get("negative_weight", -1)
            if reference["name"] != "ema" or weight != (-1 if method == "flip" else 0):
                raise ValueError(f"{directory}: metadata reference/weight does not match {method}")
            if beta is not None and not math.isclose(actual_beta, beta, abs_tol=1e-12):
                raise ValueError(f"{directory}: filename and metadata betas disagree")
            beta = actual_beta
    if seed is None or (method != "adam" and (beta is None or not 0 <= beta < 1)):
        raise ValueError(f"{directory}: seed/beta identity missing; export metadata or retain the original run name")
    return seed, beta, metadata


def load_run(method, directory, *, load_edits=True):
    directory = Path(directory).resolve()
    sources = {}
    seed, beta, metadata = identity(method, directory, sources)
    evaluations, groups = {}, {}
    path = directory / "evaluation.csv"
    previous_step, previous_seen = -1, -1
    for row in rows(path, {"step", "samples_seen", "val_top1"}, sources):
        step = numeric(row, "step", path, integer=True)
        seen = numeric(row, "samples_seen", path, integer=True)
        if step <= previous_step or seen <= previous_seen:
            raise ValueError(f"{path}: steps/samples_seen must strictly increase")
        evaluations[step] = (seen, 100 * numeric(row, "val_top1", path, maximum=1))
        previous_step, previous_seen = step, seen
    if next(iter(evaluations)) != 0 or evaluations[0][0] != 0:
        raise ValueError(f"{path}: evaluation must include initialization step 0")
    path = directory / "group_evaluation.csv"
    required = {"step", "samples_seen", "group", "label_source", "sample_count", "top1"}
    for row in rows(path, required, sources):
        group = row["group"]
        if group not in GROUPS:
            continue
        step = numeric(row, "step", path, integer=True)
        seen = numeric(row, "samples_seen", path, integer=True)
        key = (step, group)
        if key in groups or step not in evaluations or seen != evaluations[step][0]:
            raise ValueError(f"{path}: duplicate/misaligned group at {key}")
        if row["label_source"] != GROUPS[group]:
            raise ValueError(f"{path}: incorrect label_source for {group}")
        groups[key] = (numeric(row, "sample_count", path, integer=True, minimum=1),
                       100 * numeric(row, "top1", path, maximum=1))
    points, counts = [], None
    for step, (seen, test) in evaluations.items():
        if any((step, group) not in groups for group in GROUPS):
            raise ValueError(f"{path}: missing fixed group at step {step}")
        clean, original, noisy = (groups[step, group] for group in GROUPS)
        current_counts = (clean[0], original[0])
        if original[0] != noisy[0] or (counts is not None and counts != current_counts):
            raise ValueError(f"{path}: inconsistent fixed-group sample counts")
        if original[1] + noisy[1] > 100 + 1e-6:
            raise ValueError(f"{path}: corrupted original/noisy accuracies cannot sum above 100%")
        counts = current_counts
        points.append(dict(step=step, samples_seen=seen, clean_accuracy=clean[1],
                           original_accuracy=original[1], noisy_accuracy=noisy[1], test_accuracy=test))
    edits = []
    if method != "adam" and load_edits:
        path = directory / "dpcl_steps.csv"
        if not path.is_file():
            # Read old exports without renaming files, columns or provenance.
            path = directory / "dpco_steps.csv"
        prefix = "dpcl" if path.name == "dpcl_steps.csv" else "dpco"
        required = {"step", "valid_batch_size", *(f"{prefix}_{key}" for key in
                    ("edited_count", "negative_count", "negative_weight"))}
        for row in rows(path, required, sources):
            step = numeric(row, "step", path, integer=True, minimum=1)
            batch = numeric(row, "valid_batch_size", path, integer=True, minimum=1)
            edited = numeric(row, f"{prefix}_edited_count", path, integer=True, maximum=batch)
            negative = numeric(row, f"{prefix}_negative_count", path, integer=True, maximum=batch)
            weight = numeric(row, f"{prefix}_negative_weight", path, minimum=-1, maximum=0)
            if step != len(edits) + 1 or edited != negative or weight != (-1 if method == "flip" else 0):
                raise ValueError(f"{path}: noncontiguous updates or incompatible intervention/weight")
            edits.append((step, edited, batch))
        if len(edits) != points[-1]["step"]:
            raise ValueError(f"{path}: update coverage must match the last evaluation")
    return Run(method, directory, beta, seed, counts, points, edits, sources, metadata)


def comparison(runs, process_beta, endpoint_step=None):
    """Match populations, seed, evaluation budget, and complete method/beta sets."""
    cohorts = defaultdict(dict)
    if len({run.seed for run in runs}) != 1:
        raise ValueError("This beta-comparison entry requires one common training seed; do not mix seeds/betas")
    grid = [(point["step"], point["samples_seen"]) for point in runs[0].points]
    for run in runs:
        if [(p["step"], p["samples_seen"]) for p in run.points] != grid:
            raise ValueError("All runs must share the same recorded evaluation steps and samples_seen")
        key = (run.method, run.beta)
        if key in cohorts[run.counts]:
            raise ValueError(f"Duplicate method/beta within noise cohort: {run.directory}")
        cohorts[run.counts][key] = run
    beta_sets = []
    for counts, cohort in cohorts.items():
        if ("adam", None) not in cohort:
            raise ValueError(f"Noise population {counts} is missing its Adam baseline")
        flips = {b for m, b in cohort if m == "flip"}
        filters = {b for m, b in cohort if m == "filter"}
        if not flips or flips != filters or process_beta not in flips:
            raise ValueError("Each cohort needs matching Flip/Filter beta sets including --process-beta")
        beta_sets.append(flips)
    if any(betas != beta_sets[0] for betas in beta_sets):
        raise ValueError("Noise cohorts must use the same beta set")
    if len({100 * c[1] / sum(c) for c in cohorts}) != len(cohorts):
        raise ValueError("Ambiguous populations with the same noise percentage")
    endpoint = grid[-1][0] if endpoint_step is None else endpoint_step
    if endpoint not in {step for step, _ in grid}:
        raise ValueError("--endpoint-step must be an exact recorded evaluation node in every run")
    ordered = [cohorts[c] for c in sorted(cohorts, key=lambda c: c[1] / sum(c))]
    return ordered, sorted(beta_sets[0]), endpoint


def trailing(values, window):
    queue, total = deque(), 0.
    for value in values:
        queue.append(value)
        total += value
        if len(queue) > window:
            total -= queue.popleft()
        yield total / len(queue)


def edit_series(edits, window):
    """Sample-weighted trailing fraction, before display decimation."""
    queue, edited_sum, batch_sum = deque(), 0, 0
    for step, edited, batch in edits:
        queue.append((edited, batch))
        edited_sum += edited
        batch_sum += batch
        if len(queue) > window:
            old_edited, old_batch = queue.popleft()
            edited_sum -= old_edited
            batch_sum -= old_batch
        yield step, 100 * edited / batch, 100 * edited_sum / batch_sum


def csv_write(path, data):
    iterator = iter(data)
    first = next(iterator)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(first))
        writer.writeheader()
        writer.writerow(first)
        writer.writerows(iterator)


def parser():
    p = argparse.ArgumentParser(description=__doc__)
    for method in STYLES:
        p.add_argument(f"--{method}-dir", required=True, action="append", nargs="+",
                       help="Explicit directories (or run names in results/files); repeatable")
    p.add_argument("--plots", nargs="+", choices=PLOTS, default=list(PLOTS))
    p.add_argument("--process-beta", type=float, default=.96, help="Beta for process curves / optional trajectories")
    p.add_argument("--endpoint-step", type=int, help="Exact scatter evaluation step; default common final step")
    p.add_argument("--tradeoff-trajectories", action="store_true", help="Add process-beta trajectories with time arrows")
    p.add_argument("--smooth-window", type=int, default=100, help="Edited-rate trailing window in training updates")
    p.add_argument("--eval-smooth-window", type=int, default=1, help="Evaluation trailing window in recorded nodes (1=raw)")
    p.add_argument("--raw", action=argparse.BooleanOptionalAction, default=False, help="Opt in to faint raw curves under smoothing (not an uncertainty band)")
    p.add_argument("--edit-stride", type=int, default=1, help="Display/export every Nth edit point AFTER smoothing; retain endpoints")
    p.add_argument("--mark-steps", nargs="*", type=int, default=[7800], help="Vertical budget markers; e.g. 7800 is 10%% of 78000, not initialization")
    p.add_argument("--figure-width", type=float, default=5, help="Inches; height is always 0.9 times width")
    p.add_argument("--dpi", type=int, default=220)
    p.add_argument("--formats", nargs="+", choices=("png", "pdf"), default=["png", "pdf"])
    p.add_argument("--output-name", help="New subdirectory under results/figures; existing outputs are never overwritten")
    return p


def beta_colors(betas):
    """Shared rank-based shades: higher reference beta is darker in each family."""
    import matplotlib
    from matplotlib.colors import to_hex

    ordered = sorted(betas)
    levels = {beta: .5 + .4 * i / (len(ordered) - 1) if len(ordered) > 1 else .7
              for i, beta in enumerate(ordered)}
    return {method: {beta: to_hex(matplotlib.colormaps[cmap](level)) for beta, level in levels.items()}
            for method, cmap in (("flip", "Reds"), ("filter", "Oranges"))}


def render(cohorts, betas, endpoint, args, output):
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    from matplotlib.lines import Line2D

    scale = args.figure_width / 5
    plt.rcParams.update({"text.usetex": False, "font.family": "serif",
                         "font.serif": ["Nimbus Roman"], "mathtext.fontset": "cm", "font.size": 10 * scale,
                         "pdf.fonttype": 42, "axes.titlesize": 10 * scale,
                         "axes.labelsize": 10 * scale, "legend.fontsize": 8.5 * scale})
    handles = [Line2D([], [], color=color, ls=ls, label=label) for label, color, ls in STYLES.values()]
    markers = {beta: MARKERS[i % len(MARKERS)] for i, beta in enumerate(betas)}
    shades = beta_colors(betas)
    files = []

    def canvas():
        # Each exported file contains exactly one axes, never a comparison grid.
        fig, ax = plt.subplots(figsize=(args.figure_width, .9 * args.figure_width))
        fig.subplots_adjust(left=.17, right=.97, bottom=.17, top=.86)
        return fig, ax

    def finish(fig, name, legend=handles):
        fig.legend(handles=legend, loc="upper center", bbox_to_anchor=(.55, 1.),
                   ncol=min(3, len(legend)), frameon=False)
        for fmt in dict.fromkeys(args.formats):
            path = output / f"{name}.{fmt}"
            fig.savefig(path, dpi=args.dpi)
            files.append(path.name)
        plt.close(fig)

    def decorate(ax, title, xlabel, ylabel, *, step_axis=True):
        ax.set(title=title, xlabel=xlabel, ylabel=ylabel)
        ax.grid(alpha=.2)
        ax.spines[["top", "right"]].set_visible(False)
        if step_axis:
            ax.set_xlim(0, max(p["step"] for p in cohorts[0]["adam", None].points))
            ax.ticklabel_format(axis="x", style="sci", scilimits=(3, 3), useMathText=True)
            for step in args.mark_steps:
                if 0 < step <= ax.get_xlim()[1]:
                    ax.axvline(step, color=".5", lw=.6, alpha=.5, zorder=0)
                    ax.text(step, .98, f"{step:,}", transform=ax.get_xaxis_transform(),
                            rotation=90, ha="right", va="top", color=".45", fontsize=7 * scale)

    def curve(ax, run, metric):
        _, color, ls = STYLES[run.method]
        x = [p["step"] for p in run.points]
        raw = [p[metric] for p in run.points]
        if args.raw and args.eval_smooth_window > 1:
            ax.plot(x, raw, color=color, ls=ls, alpha=.18, lw=.7)
        ax.plot(x, list(trailing(raw, args.eval_smooth_window)), color=color, ls=ls, lw=1.3)

    for cohort in cohorts:
        noise = cohort["adam", None].noise_percent
        noise_name = f"noise{noise:g}".replace(".", "p")
        beta_name = f"beta{args.process_beta:g}".replace(".", "p")
        if "noise-accuracy" in args.plots:
            for metric, name, ylabel in (
                ("original_accuracy", "corrupted_original_accuracy_vs_step", "Corrupted: original acc (%)"),
                ("noisy_accuracy", "corrupted_noisy_accuracy_vs_step", "Corrupted: noisy acc (%)"),
            ):
                fig, ax = canvas()
                for method in STYLES:
                    curve(ax, cohort[method, None if method == "adam" else args.process_beta], metric)
                decorate(ax, f"{noise:g}% noise | β={args.process_beta:g}", "Training step", ylabel)
                ax.set_ylim(0, 102)
                finish(fig, f"{noise_name}_{name}_{beta_name}")

        if "test-accuracy" in args.plots:
            fig, ax = canvas()
            for method in STYLES:
                curve(ax, cohort[method, None if method == "adam" else args.process_beta], "test_accuracy")
            decorate(ax, f"{noise:g}% noise | β={args.process_beta:g}",
                     "Training step", "Clean test accuracy (%)")
            ax.set_ylim(0, 102)
            finish(fig, f"{noise_name}_clean_test_accuracy_vs_step_{beta_name}")

        if "tradeoff" in args.plots:
            fig, ax = canvas()
            for run in cohort.values():
                point = next(p for p in run.points if p["step"] == endpoint)
                _, base_color, ls = STYLES[run.method]
                color = base_color if run.method == "adam" else shades[run.method][run.beta]
                marker = "*" if run.method == "adam" else markers[run.beta]
                ax.scatter(point["clean_accuracy"], point["original_accuracy"], color=color,
                           marker=marker, s=35 * scale ** 2, zorder=4)
                index = betas.index(run.beta) if run.beta is not None else -1
                label = "Adam" if run.method == "adam" else f"β={run.beta:g}"
                # Separate annotation lanes preserve genuinely coincident points.
                clustered = point["clean_accuracy"] > 97 and point["original_accuracy"] < 5
                if clustered and run.method in ("filter", "adam"):
                    text_position = (.42, .07 + .065 * index) if run.method == "filter" else (.92, .015)
                    text_coordinates = "axes fraction"
                else:
                    text_position = (-8 * scale, (7 + 11 * index) * scale)
                    text_coordinates = "offset points"
                ax.annotate(label, (point["clean_accuracy"], point["original_accuracy"]),
                            xytext=text_position, textcoords=text_coordinates,
                            ha="right", color=color, fontsize=8 * scale,
                            arrowprops=dict(arrowstyle="-", color=color, lw=.4))
                if args.tradeoff_trajectories and (run.method == "adam" or run.beta == args.process_beta):
                    trajectory = [p for p in run.points if p["step"] <= endpoint]
                    ax.plot([p["clean_accuracy"] for p in trajectory],
                            [p["original_accuracy"] for p in trajectory], color=color, ls=ls, lw=.8, alpha=.6)
                    for i in sorted({len(trajectory) // 3, 2 * len(trajectory) // 3}):
                        if i > 0:
                            a, b = trajectory[i - 1], trajectory[i]
                            ax.annotate("", xy=(b["clean_accuracy"], b["original_accuracy"]),
                                        xytext=(a["clean_accuracy"], a["original_accuracy"]),
                                        arrowprops=dict(arrowstyle="->", color=color, lw=.8))
            title = f"{noise:g}% noise | step {endpoint:,}"
            if args.tradeoff_trajectories:
                title += f" | paths β={args.process_beta:g}"
            decorate(ax, title, "Clean training accuracy (%)", "Corrupted: original acc (%)", step_axis=False)
            ax.set_xlim(-3, 105)
            ax.set_ylim(-6, 106)
            finish(fig, f"{noise_name}_clean_vs_corrupted_original_accuracy_step{endpoint}")

        if "edit-rate" in args.plots:
            for method in ("flip", "filter"):
                fig, ax = canvas()
                label, _, ls = STYLES[method]
                for index, beta in enumerate(betas):
                    color = shades[method][beta]
                    series = list(edit_series(cohort[method, beta].edits, args.smooth_window))
                    selected = [p for i, p in enumerate(series) if i % args.edit_stride == 0 or i == len(series) - 1]
                    x, raw, smoothed = zip(*selected)
                    if args.raw and args.smooth_window > 1:
                        ax.plot(x, raw, color=color, ls=ls, alpha=.10, lw=.45)
                    ax.plot(x, smoothed, color=color, ls=ls, lw=1., marker=markers[beta],
                            markevery=(index * max(1, len(x) // (8 * len(betas))), max(1, len(x) // 8)),
                            ms=3.8 * scale, markerfacecolor="white", markeredgewidth=.7)
                decorate(ax, f"{noise:g}% noise | {label}", "Training step", "Edited contributions (%)")
                ax.set_ylim(0, 102)
                beta_handles = [Line2D([], [], color=shades[method][b], ls=ls, marker=markers[b],
                                       markerfacecolor="white", label=f"β={b:g}") for b in reversed(betas)]
                finish(fig, f"{noise_name}_{method}_edited_fraction_vs_step", beta_handles)
    return files


def main(argv=None):
    p = parser()
    args = p.parse_args(argv)
    if min(args.smooth_window, args.eval_smooth_window, args.edit_stride, args.dpi) < 1:
        p.error("windows, edit-stride and dpi must be positive")
    if not math.isfinite(args.figure_width) or args.figure_width <= 0:
        p.error("figure-width must be finite and positive")
    name = args.output_name or f"noise_training_{datetime.now():%Y%m%d_%H%M%S_%f}"
    if not re.fullmatch(r"[A-Za-z0-9][A-Za-z0-9_.-]*", name):
        p.error("output-name must be a simple directory name")
    output = ROOT / "results/figures" / name
    if output.exists():
        p.error(f"Output already exists: {output}")
    try:
        runs = [load_run(method, resolve_input(value), load_edits="edit-rate" in args.plots)
                for method in STYLES for batch in getattr(args, f"{method}_dir") for value in batch]
        cohorts, betas, endpoint = comparison(runs, args.process_beta, args.endpoint_step)
        if any(output.resolve().is_relative_to(run.directory) for run in runs):
            raise ValueError("Output cannot be inside an input run directory")
        output.mkdir(parents=True, exist_ok=False)
        files = render(cohorts, betas, endpoint, args, output)
        def evaluation_rows():
            for run in runs:
                smooth = {metric: list(trailing((point[metric] for point in run.points), args.eval_smooth_window))
                          for metric in ("clean_accuracy", "original_accuracy", "noisy_accuracy", "test_accuracy")}
                for i, point in enumerate(run.points):
                    yield dict(noise_percent=run.noise_percent, method=run.method, beta=run.beta, seed=run.seed,
                               **point, **{f"smooth_{metric}": values[i] for metric, values in smooth.items()})
        csv_write(output / "evaluation_curves.csv", evaluation_rows())
        csv_write(output / "endpoints.csv", (dict(noise_percent=run.noise_percent, method=run.method,
                  beta=run.beta, seed=run.seed, **next(p for p in run.points if p["step"] == endpoint)) for run in runs))
        if "edit-rate" in args.plots:
            def edit_rows():
                for run in runs:
                    for i, (step, raw, smooth) in enumerate(edit_series(run.edits, args.smooth_window)):
                        if i % args.edit_stride == 0 or i == len(run.edits) - 1:
                            yield dict(noise_percent=run.noise_percent, method=run.method, beta=run.beta,
                                       seed=run.seed, step=step, raw_edited_percent=raw, smooth_edited_percent=smooth)
            csv_write(output / "edited_curves.csv", edit_rows())
            csv_write(output / "intervention_summary.csv", (dict(noise_percent=run.noise_percent,
                      method=run.method, beta=run.beta, seed=run.seed, updates=len(run.edits),
                      edited_percent=100 * sum(e for _, e, _ in run.edits) / sum(b for _, _, b in run.edits))
                      for run in runs if run.edits))
        sources = {path: sha for run in runs for path, sha in run.sources.items()}
        for path, sha in sources.items():
            if hashlib.sha256(path.read_bytes()).hexdigest() != sha:
                raise ValueError(f"Input changed while plotting: {path}; output is incomplete")
        manifest = dict(status="complete", script_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
                        arguments=vars(args), beta_set=betas, endpoint_step=endpoint,
                        figure_inches=[args.figure_width, .9 * args.figure_width], figures=files,
                        layout="one axes per independent figure", beta_colors=beta_colors(betas),
                        seed=runs[0].seed, sources=[dict(path=str(path), sha256=sha) for path, sha in sources.items()],
                        runs=[dict(path=str(run.directory), method=run.method, beta=run.beta,
                                   noise_percent=run.noise_percent, counts=run.counts,
                                   metadata_available=run.metadata is not None) for run in runs],
                        semantics=dict(accuracy="percent; corrupted groups evaluate the same images against different labels",
                                       evaluation_smoothing="trailing arithmetic mean of recorded nodes, growing prefix",
                                       edit_smoothing="trailing sum(edited_count)/sum(valid_batch_size), growing prefix; before stride",
                                       endpoints="raw metrics at one common exact evaluation step; no beta averaging",
                                       beta_shades="higher beta is darker; identical red/orange mapping in edit and tradeoff figures",
                                       uncertainty="no uncertainty bands; --raw only overlays same-run unsmoothed fluctuations",
                                       test="val_top1 is the clean test metric for these CIFAR100N exports, not a tuning validation set",
                                       intervention="edited sample contributions, not detected label noise or gradient-displacement magnitude",
                                       provenance="missing metadata leaves full training settings/label-map equivalence unverified"))
        (output / "plot_manifest.json").write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n")
    except (OSError, ValueError, KeyError, ImportError) as error:
        p.exit(2, f"plot_noise_training: {error}\n")
    print(json.dumps(dict(event="noise_plots_ready", output_dir=str(output), figures=files)))
    return output


if __name__ == "__main__":
    main()
