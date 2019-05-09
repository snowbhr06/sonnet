# Copyright 2019 The Sonnet Authors. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or  implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# ============================================================================

"""Tests for sonnet.v2.src.dropout."""

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from absl.testing import parameterized
import numpy as np
from sonnet.src import dropout
from sonnet.src import test_utils
import tensorflow as tf


class DropoutTest(test_utils.TestCase, parameterized.TestCase):

  @parameterized.parameters(np.arange(.0, .9, .1))
  def test_sum_close(self, rate):
    mod = dropout.Dropout(rate=rate)
    x = tf.ones([1000])
    rtol = 0.2 if "TPU" in self.device_types else 0.1
    self.assertAllClose(
        tf.reduce_sum(mod(x, is_training=True)),
        tf.reduce_sum(mod(x, is_training=False)),
        rtol=rtol)

  @parameterized.parameters(np.arange(0, .9, .1))
  def test_dropout_rate(self, rate):
    mod = dropout.Dropout(rate=rate)
    x = tf.ones([1000])
    x = mod(x, is_training=True)

    # We should have dropped something, test we're within 10% of rate.
    # (or 20% on a TPU)
    rtol = 0.2 if "TPU" in self.device_types else 0.1
    kept = tf.math.count_nonzero(x).numpy()
    keep_prob = 1 - rate
    self.assertAllClose(kept, 1000 * keep_prob, rtol=rtol)

  def test_dropout_is_actually_random(self):
    mod = dropout.Dropout(rate=0.5)
    x = tf.ones([1000])
    tf.random.set_seed(1)
    y1 = mod(x, is_training=True)
    y2 = mod(x, is_training=True)
    self.assertNotAllClose(y1, y2)

if __name__ == "__main__":
  # tf.enable_v2_behavior()
  tf.test.main()
