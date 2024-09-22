#include <torch/extension.h>
#include <cuda.h>
#include <cuda_runtime.h>
#include <vector>

template <typename T> T ceil_div(const T x, const T y) { return x / y + !!(x % y); }

__global__ void hamming_l2_cuda_forward_kernel(
    const torch::PackedTensorAccessor32<float, 2, torch::RestrictPtrTraits> luts,
    torch::PackedTensorAccessor32<float, 1, torch::RestrictPtrTraits> output) {
  
    for (int i = blockIdx.x * blockDim.x + threadIdx.x; i < luts.size(0); i += blockDim.x * gridDim.x) {
        for (int j = blockIdx.y * blockDim.y + threadIdx.y; j < luts.size(1); j += blockDim.y * gridDim.y) {

            float l2_sum = 0;

            for(int k = j+1; k < luts.size(1); ++k) {
                auto fd = (luts[i][j] - luts[i][k]) / (__popc(j ^ k) + 1e-7);
                l2_sum += fd*fd;
            };

            atomicAdd(&output[i], l2_sum);
        
        };
    };

};

torch::Tensor hamming_l2_cuda_forward(
    torch::Tensor luts_tensor) {
  
    auto output_size = luts_tensor.size(0);
    auto luts_size = luts_tensor.size(1);

    auto output_tensor = torch::zeros({output_size}, 
    torch::TensorOptions().dtype(torch::kFloat32).device(torch::kCUDA, luts_tensor.device().index()));

    dim3 threads_per_block(32, 32);

    dim3 blocks_per_grid(
        min(static_cast<int64_t>(65535), ceil_div(output_size, static_cast<int64_t>(threads_per_block.x))),
        min(static_cast<int64_t>(65535), ceil_div(luts_size, static_cast<int64_t>(threads_per_block.y)))
    );

    hamming_l2_cuda_forward_kernel<<<blocks_per_grid, threads_per_block>>>(
        luts_tensor.packed_accessor32<float, 2, torch::RestrictPtrTraits>(),
        output_tensor.packed_accessor32<float, 1, torch::RestrictPtrTraits>()
    );

    cudaDeviceSynchronize();

    return output_tensor;
};

__global__ void hamming_l2_cuda_backward_kernel(
    const torch::PackedTensorAccessor32<float, 2, torch::RestrictPtrTraits> luts,
    torch::PackedTensorAccessor32<float, 2, torch::RestrictPtrTraits> luts_grad,
    const float gamma) {

    for (int i = blockIdx.x * blockDim.x + threadIdx.x; i < luts.size(0); i += blockDim.x * gridDim.x) {
        for (int j = blockIdx.y * blockDim.y + threadIdx.y; j < luts.size(1); j += blockDim.y * gridDim.y) {

            float l2_sum = 0;

            for(int k = 0; k < luts.size(1); ++k) {
                l2_sum += 2 * (luts[i][j] - luts[i][k]) / (__popc(j ^ k) + 1e-7);
            };

            luts_grad[i][j] = gamma * l2_sum;
        
        };
    };

};


torch::Tensor hamming_l2_cuda_backward(
    torch::Tensor luts_tensor,
    const float gamma) {
  
    auto output_size = luts_tensor.size(0);
    auto luts_size = luts_tensor.size(1);

    auto luts_grad_tensor = torch::zeros_like(luts_tensor);

    dim3 threads_per_block(32, 32);

    dim3 blocks_per_grid(
        min(static_cast<int64_t>(65535), ceil_div(output_size, static_cast<int64_t>(threads_per_block.x))),
        min(static_cast<int64_t>(65535), ceil_div(luts_size, static_cast<int64_t>(threads_per_block.y)))
    );

    hamming_l2_cuda_backward_kernel<<<blocks_per_grid, threads_per_block>>>(
        luts_tensor.packed_accessor32<float, 2, torch::RestrictPtrTraits>(),
        luts_grad_tensor.packed_accessor32<float, 2, torch::RestrictPtrTraits>(),
        gamma
    );

    cudaDeviceSynchronize();

    return luts_grad_tensor;
};



