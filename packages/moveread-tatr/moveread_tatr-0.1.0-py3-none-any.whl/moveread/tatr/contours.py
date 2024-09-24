import torch
from jaxtyping import Float

def corner2center(bboxes: Float[torch.Tensor, 'N 4']) -> Float[torch.Tensor, 'N 4']:
  """`(x1, y1, x2, y2) -> (center_x, center_y, width, height)`"""
  top_left_x, top_left_y, bottom_right_x, bottom_right_y = bboxes.unbind(-1)
  b = [
    (top_left_x + bottom_right_x) / 2,  # center x
    (top_left_y + bottom_right_y) / 2,  # center y
    (bottom_right_x - top_left_x),  # width
    (bottom_right_y - top_left_y),  # height
  ]
  return torch.stack(b, dim=-1)

def center2corner(bboxes: Float[torch.Tensor, 'N 4']) -> Float[torch.Tensor, 'N 4']:
  """`(center_x, center_y, width, height) -> (x1, y1, x2, y2)`"""
  center_x, center_y, width, height = bboxes.unbind(-1)
  return torch.stack(
    # top left x, top left y, bottom right x, bottom right y
    [(center_x - 0.5 * width), (center_y - 0.5 * height), (center_x + 0.5 * width), (center_y + 0.5 * height)],
    dim=-1,
  )

def contours2bbox(cnts: Float[torch.Tensor, 'N 4 2']) -> Float[torch.Tensor, 'N 4']:
  min_xy = cnts.min(dim=1).values  # (N, 2)
  max_xy = cnts.max(dim=1).values  # (N, 2)
  # Combine (x_min, y_min, x_max, y_max) into a single tensor
  return torch.cat([min_xy, max_xy], dim=1) # (N, 4)

def bbox2contours(bboxes: Float[torch.Tensor, 'N 4']) -> Float[torch.Tensor, 'N 4 2']:
  """Convert bounding boxes to contours"""
  return torch.stack([
    bboxes[..., [0, 1]],
    bboxes[..., [2, 1]],
    bboxes[..., [2, 3]],
    bboxes[..., [0, 3]],
  ], dim=1)  # (N, 4, 2)