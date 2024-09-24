import torch
import pure_cv as vc
from torchvision import transforms

normalize = transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])

def img2tensor(img: vc.Img):
  """Convert an image to a normalized tensor. `img` must already be resized."""
  return torch.tensor(img).float().permute(2, 0, 1)

def preprocess(img: vc.Img) -> torch.Tensor:
  img = vc.descale_h(img, 1024)
  return normalize(img2tensor(img) / 255.0)
