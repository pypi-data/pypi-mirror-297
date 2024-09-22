#include <torch/extension.h>

#include <vector>

torch::Tensor hamming_l2_cuda_forward(
    torch::Tensor luts);

torch::Tensor hamming_l2_cuda_backward(
    torch::Tensor luts,
    const float gamma);

#define CHECK_CUDA(x) TORCH_CHECK(x.device().is_cuda(), #x " must be a CUDA tensor")
#define CHECK_CONTIGUOUS(x) TORCH_CHECK(x.is_contiguous(), #x " must be contiguous")
#define CHECK_INPUT(x) CHECK_CUDA(x); CHECK_CONTIGUOUS(x)

torch::Tensor hamming_l2_forward(
    torch::Tensor luts) {
  CHECK_INPUT(luts);
  return hamming_l2_cuda_forward(luts);
};

torch::Tensor hamming_l2_backward(
    torch::Tensor luts,
    const float gamma) {
  CHECK_INPUT(luts);
  return hamming_l2_cuda_backward(luts, gamma);
};

PYBIND11_MODULE(TORCH_EXTENSION_NAME, m) {
  m.def("forward", &hamming_l2_forward, "Hamming L2 CUDA forward");
  m.def("backward", &hamming_l2_backward, "Hamming L2 CUDA backward");
}