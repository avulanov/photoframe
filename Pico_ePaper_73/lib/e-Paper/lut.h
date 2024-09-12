//
// Copyright 2024 Wenting Zhang <zephray@outlook.com>
//
// Permission is hereby granted, free of charge, to any person obtaining a copy
// of this software and associated documentation files (the "Software"), to deal
// in the Software without restriction, including without limitation the rights
// to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
// copies of the Software, and to permit persons to whom the Software is
// furnished to do so, subject to the following conditions:
//
// The above copyright notice and this permission notice shall be included in
// all copies or substantial portions of the Software.
//
// THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
// IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
// FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
// AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
// LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
// OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
// SOFTWARE.
//
#pragma once

#include <stdint.h>

#define VCOM_LUT_SIZE   220
#define COLOR_LUT_SIZE  260
#define XON_LUT_SIZE    200

#define VCOM_LUT_REG    0x20
#define XON_LUT_REG     0x29

typedef struct {
    const uint8_t *lut;
    uint32_t size;
} lut_t;


extern const uint8_t lut0_vcom_20[11];
extern const uint8_t lut0_c0_21[13];
extern const uint8_t lut0_c3_22[13];
extern const uint8_t lut0_c1_23[13];
extern const uint8_t lut0_c2_24[13];
extern const uint8_t lut0_c4_25[13];
extern const uint8_t lut0_c5_26[13];
extern const uint8_t lut0_c6_27[13];
extern const uint8_t lut0_c7_28[13];
extern const uint8_t lut0_xon_29[10];

extern const uint8_t lut1_vcom_20[11];
extern const uint8_t lut1_c0_21[13];
extern const uint8_t lut1_c3_22[13];
extern const uint8_t lut1_c1_23[13];
extern const uint8_t lut1_c2_24[13];
extern const uint8_t lut1_c4_25[13];
extern const uint8_t lut1_c5_26[13];
extern const uint8_t lut1_c6_27[13];
extern const uint8_t lut1_c7_28[13];
extern const uint8_t lut1_xon_29[10];

extern const lut_t lut0[10];
extern const lut_t lut1[10];

