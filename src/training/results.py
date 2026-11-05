"""Shared result paths; recording schemas and checkpoint policies are separate."""

from dataclasses import dataclass
from pathlib import Path
from datetime import datetime
import re


def safe_component(value, field):
    if not isinstance(value, str) or not re.fullmatch(r"[A-Za-z0-9_.-]+", value) or value in (".", ".."):
        raise ValueError(f"{field} must be one safe directory component")
    return value


def edit_budget_label(bottom_k, bottom_k_percent):
    if bottom_k is not None:
        return f"k{bottom_k}"
    if bottom_k_percent is not None:
        return "kpct" + format(bottom_k_percent, ".12g").replace("+", "")
    return None


def infer_result_group(dataset, *, bottom_k, bottom_k_percent, has_ema):
    dataset = "digit" if dataset == "digits" else dataset
    budget = edit_budget_label(bottom_k, bottom_k_percent)
    if budget is not None:
        return f"{dataset}_{budget}"
    return f"{dataset}_allneg" if has_ema else dataset


@dataclass(frozen=True)
class ResultsPaths:
    root: Path
    group: str | None = None

    def __post_init__(self):
        if self.group is not None:
            safe_component(self.group, "result_group")

    @classmethod
    def resolve(cls, root_dir: str, *, base_dir: Path, group=None):
        """Resolve relative output roots against an explicit project directory."""
        root = Path(root_dir).expanduser()
        if not root.is_absolute():
            root = Path(base_dir) / root
        return cls(root.resolve(), group)

    def _stream(self, name):
        stream = self.root / name
        return stream / self.group if self.group is not None else stream

    @property
    def logs(self) -> Path:
        return self._stream("logs")

    @property
    def runs(self) -> Path:
        return self._stream("runs")

    @property
    def files(self) -> Path:
        return self._stream("files")

    def create(self) -> None:
        """Create directories only; never write logs, checkpoints, or CSV data."""
        for path in (self.logs, self.runs, self.files):
            path.mkdir(parents=True, exist_ok=True)

    def experiment(self, run_name):
        return ExperimentPaths(self, safe_component(run_name, "run_name"))

    def find_resume(self, run_name):
        """Resolve one complete run, checking both grouped and legacy flat locations."""
        initial = self.experiment(run_name)
        if self.group is not None:
            candidates = [initial]
        else:
            candidates = [initial]
            if self.runs.is_dir():
                candidates.extend(ResultsPaths(self.root, path.name).experiment(run_name)
                    for path in self.runs.iterdir()
                    if (path / run_name).is_dir() and re.fullmatch(r"[A-Za-z0-9_.-]+", path.name))
        matches = [paths for paths in candidates if all(
            directory.is_dir() for directory in (paths.logs, paths.runs, paths.files))]
        if not matches:
            raise FileNotFoundError(f"No complete result directories for resume run {run_name!r}")
        if len(matches) != 1:
            raise ValueError(f"Resume run {run_name!r} exists in multiple locations; specify --result-group")
        return matches[0]


def method_label(config):
    """Label optimizer and EMA weights without changing historical SGD labels."""
    label = config.method.name
    if label == "dpcl_policy":
        label = "dpcl_" + ("e" if config.reference.name == "error" else "l") + "_" + config.method.policy_mode
        if config.method.policy_mode == "alternating" and config.method.alternating_first == "dpcl":
            label += "_first_dpcl"
    if config.reference.name == "ema":
        label = "dpcl_ema_b" + format(config.reference.beta, ".12g") + "_w" + format(config.method.negative_weight, ".12g").replace("+", "")
        budget = edit_budget_label(config.method.bottom_k, config.method.bottom_k_percent)
        if budget is not None:
            label += "_" + budget
    elif label in ("dpcl", "dpcl_loo", "dtv", "dtv_loo"):
        suffix = {"error": "_e", "loss": "_l", "correct": "_r"}[config.reference.name]
        label = label.replace("_loo", "") + suffix + ("_loo" if label.endswith("_loo") else "")
    if config.method.dpcl_warmup_percent:
        label += "_warmup" + format(config.method.dpcl_warmup_percent, ".12g") + "pct"
    if config.training.optimizer == "adam" and config.method.name != "adam":
        label += "_adam"
    return label


def make_run_name(config, *, timestamp=None):
    """Use one timezone-aware timestamp across all three experiment directories."""
    timestamp = timestamp or datetime.now().astimezone()
    label = method_label(config)
    parts = (config.data.name, config.data.mode, config.model.name, label,
             str(config.seed), format(config.training.learning_rate, ".12g"))
    if config.data.name == "cifar100n":
        parts += (config.data.noise_type, "human" if config.data.is_human else f"synthetic_s{config.data.noise_seed}")
    elif config.data.name in ("mnist", "digits"):
        parts += ("symmetric" + format(config.data.label_noise_percent, ".12g"),
                  f"noise_s{config.data.noise_seed}")
    elif config.data.name == "cnwl":
        parts += ("red" + str(config.data.cnwl_noise_percent), "official_split")
    elif config.data.noise_manifest:
        parts += ("clip_idn",)
    # Label newly created decaying-rate runs in logs/files/runs and lifecycle
    # records. Constant names and explicit historical resume names stay unchanged.
    if config.training.lr_schedule != "constant":
        parts += (config.training.lr_schedule,)
    parts += (timestamp.strftime("%Y%m%d_%H%M%S"),)
    name = "_".join(parts)
    if not re.fullmatch(r"[A-Za-z0-9_.-]+", name):
        raise ValueError("Run-name fields must be safe directory components")
    return name


@dataclass(frozen=True)
class ExperimentPaths:
    parent: ResultsPaths
    name: str

    @property
    def logs(self):
        return self.parent.logs / self.name

    @property
    def runs(self):
        return self.parent.runs / self.name

    @property
    def files(self):
        return self.parent.files / self.name

    def create(self, *, resume=False):
        paths = (self.logs, self.runs, self.files)
        if resume:
            if not all(path.is_dir() for path in paths):
                raise FileNotFoundError("Resume requires all existing experiment directories")
        else:
            if any(path.exists() for path in paths):
                raise FileExistsError(f"Experiment already exists: {self.name}")
            for path in paths:
                path.mkdir(parents=True, exist_ok=False)

    def reserve(self):
        """Reserve a new run before nohup opens its persistent stdout file."""
        self.create()
        (self.runs / ".launch_reserved").touch(exist_ok=False)

    def claim_reserved(self):
        if not all(path.is_dir() for path in (self.logs, self.runs, self.files)):
            raise FileNotFoundError("Missing launch reservation directories")
        if (self.logs / "metadata.json").exists():
            raise FileExistsError("A new launch must not overwrite an existing run")
        (self.runs / ".launch_reserved").unlink()
