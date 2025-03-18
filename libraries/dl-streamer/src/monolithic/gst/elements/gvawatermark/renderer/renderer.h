/*******************************************************************************
 * Copyright (C) 2020-2022 Intel Corporation
 *
 * SPDX-License-Identifier: MIT
 ******************************************************************************/

#pragma once

#include "color_converter.h"

#include "render_prim.h"
#include <dlstreamer/frame.h>

#include <memory>
#include <stdexcept>
#include <vector>

class Renderer {
  public:
    void draw(dlstreamer::FramePtr buffer, std::vector<render::Prim> prims);

    virtual ~Renderer() = default;

  protected:
    std::shared_ptr<ColorConverter> _color_converter;

    Renderer(std::shared_ptr<ColorConverter> color_converter) : _color_converter(color_converter) {
    }

    void convert_prims_color(std::vector<render::Prim> &prims);

    virtual void draw_backend(std::vector<cv::Mat> &image_planes, std::vector<render::Prim> &prims) = 0;
    virtual dlstreamer::FramePtr buffer_map(dlstreamer::FramePtr buffer) = 0;

  private:
    static int FourccToOpenCVMatType(int fourcc);

    static std::vector<cv::Mat> convertBufferToCvMats(dlstreamer::Frame &buffer);
};
