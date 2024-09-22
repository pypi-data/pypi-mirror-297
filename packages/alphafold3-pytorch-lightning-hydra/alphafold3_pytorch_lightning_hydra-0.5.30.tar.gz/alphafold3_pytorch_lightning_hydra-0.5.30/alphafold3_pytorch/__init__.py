import importlib

from beartype.typing import Any, List, Set
from omegaconf import OmegaConf

from alphafold3_pytorch.cli import cli
from alphafold3_pytorch.data.pdb_datamodule import (
    alphafold3_input_to_biomolecule,
    alphafold3_inputs_to_batched_atom_input,
    collate_inputs_to_batched_atom_input,
    pdb_inputs_to_batched_atom_input,
)
from alphafold3_pytorch.models.alphafold3_module import Alphafold3LitModule
from alphafold3_pytorch.models.components.alphafold3 import (
    AdaptiveLayerNorm,
    Alphafold3,
    Alphafold3WithHubMixin,
    AttentionPairBias,
    CentreRandomAugmentation,
    ComputeAlignmentError,
    ComputeModelSelectionScore,
    ComputeRankingScore,
    ConditionWrapper,
    ConfidenceHead,
    ConfidenceHeadLogits,
    DiffusionModule,
    DiffusionTransformer,
    DistogramHead,
    ElucidatedAtomDiffusion,
    InputFeatureEmbedder,
    MSAModule,
    MSAPairWeightedAveraging,
    MultiChainPermutationAlignment,
    OuterProductMean,
    PairformerStack,
    PreLayerNorm,
    RelativePositionEncoding,
    SmoothLDDTLoss,
    TemplateEmbedder,
    Transition,
    TriangleAttention,
    TriangleMultiplication,
    WeightedRigidAlign,
)
from alphafold3_pytorch.models.components.attention import (
    Attend,
    Attention,
    full_pairwise_repr_to_windowed,
)
from alphafold3_pytorch.models.components.inputs import (
    CONSTRAINT_DIMS,
    Alphafold3Input,
    AtomDataset,
    AtomInput,
    BatchedAtomInput,
    MoleculeInput,
    PDBDataset,
    PDBInput,
    atom_input_to_file,
    file_to_atom_input,
    maybe_transform_to_atom_input,
    maybe_transform_to_atom_inputs,
    pdb_dataset_to_atom_inputs,
    register_input_transform,
)
from alphafold3_pytorch.utils.model_utils import (
    ExpressCoordinatesInFrame,
    RigidFrom3Points,
    RigidFromReference3Points,
)

__all__ = [
    Attention,
    Attend,
    RelativePositionEncoding,
    SmoothLDDTLoss,
    WeightedRigidAlign,
    MultiChainPermutationAlignment,
    ExpressCoordinatesInFrame,
    RigidFrom3Points,
    RigidFromReference3Points,
    ComputeAlignmentError,
    CentreRandomAugmentation,
    TemplateEmbedder,
    PreLayerNorm,
    AdaptiveLayerNorm,
    ConditionWrapper,
    OuterProductMean,
    MSAPairWeightedAveraging,
    TriangleMultiplication,
    AttentionPairBias,
    TriangleAttention,
    Transition,
    MSAModule,
    PairformerStack,
    DiffusionTransformer,
    DiffusionModule,
    ElucidatedAtomDiffusion,
    InputFeatureEmbedder,
    ComputeRankingScore,
    ConfidenceHead,
    ConfidenceHeadLogits,
    ComputeModelSelectionScore,
    DistogramHead,
    Alphafold3,
    Alphafold3WithHubMixin,
    Alphafold3LitModule,
    AtomInput,
    BatchedAtomInput,
    MoleculeInput,
    Alphafold3Input,
    AtomDataset,
    PDBInput,
    PDBDataset,
    alphafold3_inputs_to_batched_atom_input,
    alphafold3_input_to_biomolecule,
    atom_input_to_file,
    cli,
    collate_inputs_to_batched_atom_input,
    file_to_atom_input,
    full_pairwise_repr_to_windowed,
    maybe_transform_to_atom_input,
    maybe_transform_to_atom_inputs,
    pdb_dataset_to_atom_inputs,
    pdb_inputs_to_batched_atom_input,
    register_input_transform,
]


def resolve_omegaconf_variable(variable_path: str) -> Any:
    """Resolve an OmegaConf variable path to its value."""
    try:
        # split the string into parts using the dot separator
        parts = variable_path.rsplit(".", 1)

        # get the module name from the first part of the path
        module_name = parts[0]

        # dynamically import the module using the module name
        try:
            module = importlib.import_module(module_name)
            # use the imported module to get the requested attribute value
            attribute = getattr(module, parts[1])
        except Exception:
            module = importlib.import_module(".".join(module_name.split(".")[:-1]))
            inner_module = ".".join(module_name.split(".")[-1:])
            # use the imported module to get the requested attribute value
            attribute = getattr(getattr(module, inner_module), parts[1])

    except Exception as e:
        raise ValueError(
            f"Error: {variable_path} is not a valid path to a Python variable within the project."
        ) from e

    return attribute


def resolve_omegaconf_classes(module_name: str, class_names: List[str]) -> Set[Any]:
    """Resolve an OmegaConf module name to its requested classes."""
    try:
        classes = set()
        # dynamically import the module using the module name
        try:
            module = importlib.import_module(module_name)
            # use the imported module to get the requested classes
            for class_name in class_names:
                classes.add(getattr(module, class_name))
        except Exception:
            module = importlib.import_module(".".join(module_name.split(".")[:-1]))
            inner_module = ".".join(module_name.split(".")[-1:])
            # use the imported inner module to get the requested classes alternatively
            for class_name in class_names:
                classes.add(getattr(getattr(module, inner_module), class_name))

    except Exception as e:
        raise ValueError(
            f"Error: {module_name} is not a valid path to a Python module within the project."
        ) from e

    return classes


def int_divide(x: int, y: int, raise_exception: bool = False) -> int:
    """Perform integer division on `x` and `y`.

    :param x: The dividend.
    :param y: The divisor.
    :return: The integer division result.
    """
    if x % y == 0 or not raise_exception:
        return x // y
    elif x % y != 0 and raise_exception:
        raise ValueError(
            f"Error: {x} is not divisible by {y} in the call to OmegaConf's `int_divide` function."
        )


def register_custom_omegaconf_resolvers():
    """Register custom OmegaConf resolvers."""
    OmegaConf.register_new_resolver(
        "resolve_variable", lambda variable_path: resolve_omegaconf_variable(variable_path)
    )
    OmegaConf.register_new_resolver(
        "resolve_classes",
        lambda module_name, class_names: resolve_omegaconf_classes(module_name, class_names),
    )
    OmegaConf.register_new_resolver(
        "resolve_list_as_tuple",
        lambda object_list: tuple(object_list),
    )
    OmegaConf.register_new_resolver("add", lambda x, y: x + y)
    OmegaConf.register_new_resolver("subtract", lambda x, y: x - y)
    OmegaConf.register_new_resolver("multiply", lambda x, y: x * y)
    OmegaConf.register_new_resolver("divide", lambda x, y: x / y)
    OmegaConf.register_new_resolver("int_divide", lambda x, y: int_divide(int(x), int(y)))
