from .color_cluster.model import ColorClusterModel

try:
    from .resunet_torch.model import ResUNetTorch
except ImportError:
    print(
        "failed to import ResUnetTorch model. Please install PyTorch if you want to use it."
    )
