/*******************************************************************************
 * Copyright (C) 2023 Intel Corporation
 *
 * SPDX-License-Identifier: MIT
 ******************************************************************************/

#pragma once

#include <gst/gst.h>
#include <gst/gsttracer.h>

G_BEGIN_DECLS

#define LATENCY_TRACER_TYPE (latency_tracer_get_type())
#define LATENCY_TRACER(obj) (G_TYPE_CHECK_INSTANCE_CAST((obj), LATENCY_TRACER_TYPE, LatencyTracer))
#define LATENCY_TRACER_CLASS(klass) (G_TYPE_CHECK_CLASS_CAST((klass), LATENCY_TRACER_TYPE, LatencyTracerClass))
#define IS_LATENCY_TRACER(obj) (G_TYPE_CHECK_INSTANCE_TYPE((obj), LATENCY_TRACER_TYPE))
#define IS_LATENCY_TRACER_CLASS(klass) (G_TYPE_CHECK_CLASS_TYPE((klass), LATENCY_TRACER_TYPE))
#define LATENCY_TRACER_CAST(obj) ((LatencyTracer *)(obj))

typedef enum {
    LATENCY_TRACER_FLAG_PIPELINE = 1 << 0,
    LATENCY_TRACER_FLAG_ELEMENT = 1 << 1,
} LatencyTracerFlags;

struct LatencyTracer {
    GstTracer parent;

    /*< private >*/
    GstElement *pipeline;
    GstElement *sink_element;
    guint frame_count;
    gdouble toal_latency;
    gdouble min;
    gdouble max;
    gdouble interval_total;
    gdouble interval_min;
    gdouble interval_max;
    guint interval_frame_count;
    GstClockTime interval_init_time;
    gint interval;
    GstClockTime first_frame_init_ts;
    LatencyTracerFlags flags;
};

struct LatencyTracerClass {
    GstTracerClass parent_class;
};

G_GNUC_INTERNAL GType latency_tracer_get_type(void);

G_END_DECLS
