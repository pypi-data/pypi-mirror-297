/* SPDX-License-Identifier: MIT
 *
 * Permission is hereby granted, free of charge, to any person
 * obtaining a copy of this software and associated documentation
 * files (the "Software"), to deal in the Software without
 * restriction, including without limitation the rights to use, copy,
 * modify, merge, publish, distribute, sublicense, and/or sell copies
 * of the Software, and to permit persons to whom the Software is
 * furnished to do so, subject to the following conditions:
 *
 * The above copyright notice and this permission notice shall be
 * included in all copies or substantial portions of the Software.
 *
 * THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
 * EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
 * MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
 * NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS
 * BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN
 * ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN
 * CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
 * SOFTWARE.
 *
 * Copyright:
 *   2020      Evan Nemerson <evan@nemerson.com>
 */

#if !defined(SIMDE_ARM_NEON_MAXNM_H)
#define SIMDE_ARM_NEON_MAXNM_H

#include "types.h"
#include "cge.h"
#include "bsl.h"

HEDLEY_DIAGNOSTIC_PUSH
SIMDE_DISABLE_UNWANTED_DIAGNOSTICS
SIMDE_BEGIN_DECLS_

SIMDE_FUNCTION_ATTRIBUTES
simde_float32x2_t
simde_vmaxnm_f32(simde_float32x2_t a, simde_float32x2_t b) {
  #if defined(SIMDE_ARM_NEON_A32V8_NATIVE) && (__ARM_NEON_FP >= 6)
    return vmaxnm_f32(a, b);
  #else
    simde_float32x2_private
      r_,
      a_ = simde_float32x2_to_private(a),
      b_ = simde_float32x2_to_private(b);

    SIMDE_VECTORIZE
    for (size_t i = 0 ; i < (sizeof(r_.values) / sizeof(r_.values[0])) ; i++) {
      #if defined(simde_math_fmaxf)
        r_.values[i] = simde_math_fmaxf(a_.values[i], b_.values[i]);
      #else
        if (a_.values[i] > b_.values[i]) {
          r_.values[i] = a_.values[i];
        } else if (a_.values[i] < b_.values[i]) {
          r_.values[i] = b_.values[i];
        } else if (a_.values[i] == a_.values[i]) {
          r_.values[i] = a_.values[i];
        } else {
          r_.values[i] = b_.values[i];
        }
      #endif
    }

    return simde_float32x2_from_private(r_);
  #endif
}
#if defined(SIMDE_ARM_NEON_A32V7_ENABLE_NATIVE_ALIASES)
  #undef vmaxnm_f32
  #define vmaxnm_f32(a, b) simde_vmaxnm_f32((a), (b))
#endif

SIMDE_FUNCTION_ATTRIBUTES
simde_float64x1_t
simde_vmaxnm_f64(simde_float64x1_t a, simde_float64x1_t b) {
  #if defined(SIMDE_ARM_NEON_A64V8_NATIVE)
    return vmaxnm_f64(a, b);
  #else
    simde_float64x1_private
      r_,
      a_ = simde_float64x1_to_private(a),
      b_ = simde_float64x1_to_private(b);

    SIMDE_VECTORIZE
    for (size_t i = 0 ; i < (sizeof(r_.values) / sizeof(r_.values[0])) ; i++) {
      #if defined(simde_math_fmax)
        r_.values[i] = simde_math_fmax(a_.values[i], b_.values[i]);
      #else
        if (a_.values[i] > b_.values[i]) {
          r_.values[i] = a_.values[i];
        } else if (a_.values[i] < b_.values[i]) {
          r_.values[i] = b_.values[i];
        } else if (a_.values[i] == a_.values[i]) {
          r_.values[i] = a_.values[i];
        } else {
          r_.values[i] = b_.values[i];
        }
      #endif
    }

    return simde_float64x1_from_private(r_);
  #endif
}
#if defined(SIMDE_ARM_NEON_A64V8_ENABLE_NATIVE_ALIASES)
  #undef vmaxnm_f64
  #define vmaxnm_f64(a, b) simde_vmaxnm_f64((a), (b))
#endif

SIMDE_FUNCTION_ATTRIBUTES
simde_float32x4_t
simde_vmaxnmq_f32(simde_float32x4_t a, simde_float32x4_t b) {
  #if defined(SIMDE_ARM_NEON_A32V8_NATIVE) && (__ARM_NEON_FP >= 6)
    return vmaxnmq_f32(a, b);
  #elif defined(SIMDE_POWER_ALTIVEC_P6_NATIVE)
    return vec_max(a, b);
  #else
    simde_float32x4_private
      r_,
      a_ = simde_float32x4_to_private(a),
      b_ = simde_float32x4_to_private(b);

    #if defined(SIMDE_X86_SSE_NATIVE)
      #if !defined(SIMDE_FAST_NANS)
        __m128 r = _mm_max_ps(a_.m128, b_.m128);
        __m128 bnan = _mm_cmpunord_ps(b_.m128, b_.m128);
        r = _mm_andnot_ps(bnan, r);
        r = _mm_or_ps(r, _mm_and_ps(a_.m128, bnan));
        r_.m128 = r;
      #else
        r_.m128 = _mm_max_ps(a_.m128, b_.m128);
      #endif
    #elif defined(SIMDE_WASM_SIMD128_NATIVE) && defined(SIMDE_FAST_NANS)
      r_.v128 = wasm_f32x4_max(a_.v128, b_.v128);
    #else
      SIMDE_VECTORIZE
      for (size_t i = 0 ; i < (sizeof(r_.values) / sizeof(r_.values[0])) ; i++) {
        #if defined(simde_math_fmaxf)
          r_.values[i] = simde_math_fmaxf(a_.values[i], b_.values[i]);
        #else
          if (a_.values[i] > b_.values[i]) {
            r_.values[i] = a_.values[i];
          } else if (a_.values[i] < b_.values[i]) {
            r_.values[i] = b_.values[i];
          } else if (a_.values[i] == a_.values[i]) {
            r_.values[i] = a_.values[i];
          } else {
            r_.values[i] = b_.values[i];
          }
        #endif
      }
    #endif

    return simde_float32x4_from_private(r_);
  #endif
}
#if defined(SIMDE_ARM_NEON_A32V7_ENABLE_NATIVE_ALIASES)
  #undef vmaxnmq_f32
  #define vmaxnmq_f32(a, b) simde_vmaxnmq_f32((a), (b))
#endif

SIMDE_FUNCTION_ATTRIBUTES
simde_float64x2_t
simde_vmaxnmq_f64(simde_float64x2_t a, simde_float64x2_t b) {
  #if defined(SIMDE_ARM_NEON_A64V8_NATIVE)
    return vmaxnmq_f64(a, b);
  #elif defined(SIMDE_POWER_ALTIVEC_P7_NATIVE)
    return vec_max(a, b);
  #else
    simde_float64x2_private
      r_,
      a_ = simde_float64x2_to_private(a),
      b_ = simde_float64x2_to_private(b);

    #if defined(SIMDE_X86_SSE2_NATIVE)
      #if !defined(SIMDE_FAST_NANS)
        __m128d r = _mm_max_pd(a_.m128d, b_.m128d);
        __m128d bnan = _mm_cmpunord_pd(b_.m128d, b_.m128d);
        r = _mm_andnot_pd(bnan, r);
        r = _mm_or_pd(r, _mm_and_pd(a_.m128d, bnan));
        r_.m128d = r;
      #else
        r_.m128d = _mm_max_pd(a_.m128d, b_.m128d);
      #endif
    #elif defined(SIMDE_WASM_SIMD128_NATIVE) && defined(SIMDE_FAST_NANS)
      r_.v128 = wasm_f64x2_max(a_.v128, b_.v128);
    #else
      SIMDE_VECTORIZE
      for (size_t i = 0 ; i < (sizeof(r_.values) / sizeof(r_.values[0])) ; i++) {
        #if defined(simde_math_fmax)
          r_.values[i] = simde_math_fmax(a_.values[i], b_.values[i]);
        #else
          if (a_.values[i] > b_.values[i]) {
            r_.values[i] = a_.values[i];
          } else if (a_.values[i] < b_.values[i]) {
            r_.values[i] = b_.values[i];
          } else if (a_.values[i] == a_.values[i]) {
            r_.values[i] = a_.values[i];
          } else {
            r_.values[i] = b_.values[i];
          }
        #endif
      }
    #endif

    return simde_float64x2_from_private(r_);
  #endif
}
#if defined(SIMDE_ARM_NEON_A64V8_ENABLE_NATIVE_ALIASES)
  #undef vmaxnmq_f64
  #define vmaxnmq_f64(a, b) simde_vmaxnmq_f64((a), (b))
#endif

SIMDE_END_DECLS_
HEDLEY_DIAGNOSTIC_POP

#endif /* !defined(SIMDE_ARM_NEON_MAXNM_H) */
