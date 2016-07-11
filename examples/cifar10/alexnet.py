# Licensed to the Apache Software Foundation (ASF) under one
# or more contributor license agreements.  See the NOTICE file
# distributed with this work for additional information
# regarding copyright ownership.  The ASF licenses this file
# to you under the Apache License, Version 2.0 (the
# "License"); you may not use this file except in compliance
# with the License.  You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# =============================================================================
import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), '../../build/python'))
from singa import layer
from singa import metric
from singa import loss
from singa import net as ffnet
from singa.proto import core_pb2


def create_net():
    net = ffnet.FeedForwardNet(loss.SoftmaxCrossEntropy(), metric.Accuracy())
    W0_specs = {'init': 'gaussian', 'mean': 0, 'std': 0.0001}
    W1_specs = {'init': 'gaussian', 'mean': 0, 'std': 0.01}
    W2_specs = {'init': 'gaussian', 'mean': 0, 'std': 0.01, 'decay_mult': 250}
    b_specs = {'init': 'constant', 'value': 0, 'lt_mult': 2}
    net.add(layer.Conv2D('conv1', 32, 5, 1, W_specs=W0_specs.copy(), b_specs=b_specs.copy(), pad=2, input_sample_shape=(3,32,32,)))
    net.add(layer.MaxPooling2D('pool1', 3, 2, pad=1))
    net.add(layer.Activation('relu1'))
    net.add(layer.LRN(name='lrn1'))
    net.add(layer.Conv2D('conv2', 32, 5, 1, W_specs=W1_specs.copy(), b_specs=b_specs.copy(), pad=2))
    net.add(layer.Activation('relu2'))
    net.add(layer.MaxPooling2D('pool2', 3, 2,  pad=1))
    net.add(layer.LRN('lrn2'))
    net.add(layer.Conv2D('conv3', 64, 5, 1, W_specs=W1_specs.copy(), b_specs=b_specs.copy(), pad=2))
    net.add(layer.Activation('relu3'))
    net.add(layer.MaxPooling2D('pool3', 3, 2, pad=1))
    net.add(layer.Flatten('flat'))
    net.add(layer.Dense('dense', 10, W_specs=W2_specs.copy(), b_specs=b_specs.copy()))
    return net