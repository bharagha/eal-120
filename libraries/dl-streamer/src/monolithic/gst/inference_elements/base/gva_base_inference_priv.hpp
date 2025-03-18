/*******************************************************************************
 * Copyright (C) 2022-2024 Intel Corporation
 *
 * SPDX-License-Identifier: MIT
 ******************************************************************************/

#pragma once

#ifdef __cplusplus

#include "inference_backend/buffer_mapper.h"

#include <memory>

// Channel (GvaBaseInference) specific information. Contains C++ objects
struct GvaBaseInferencePrivate {
    // Decoder VA display, if present
    dlstreamer::ContextPtr va_display;

    std::unique_ptr<InferenceBackend::BufferToImageMapper> buffer_mapper;
};

#endif // __cplusplus
