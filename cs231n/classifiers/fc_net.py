from builtins import range
from builtins import object
import numpy as np

from ..layers import *
from ..layer_utils import *


class TwoLayerNet(object):
    """
    A two-layer fully-connected neural network with ReLU nonlinearity and
    softmax loss that uses a modular layer design. We assume an input dimension
    of D, a hidden dimension of H, and perform classification over C classes.

    The architecure should be affine - relu - affine - softmax.

    Note that this class does not implement gradient descent; instead, it
    will interact with a separate Solver object that is responsible for running
    optimization.

    The learnable parameters of the model are stored in the dictionary
    self.params that maps parameter names to numpy arrays.
    """

    def __init__(
        self,
        input_dim=3 * 32 * 32,
        hidden_dim=100,
        num_classes=10,
        weight_scale=1e-3,
        reg=0.0,
    ):
        """
        Initialize a new network.

        Inputs:
        - input_dim: An integer giving the size of the input
        - hidden_dim: An integer giving the size of the hidden layer
        - num_classes: An integer giving the number of classes to classify
        - weight_scale: Scalar giving the standard deviation for random
          initialization of the weights.
        - reg: Scalar giving L2 regularization strength.
        """
        self.params = {}
        self.reg = reg

        ############################################################################
        # TODO: Initialize the weights and biases of the two-layer net. Weights    #
        # should be initialized from a Gaussian centered at 0.0 with               #
        # standard deviation equal to weight_scale, and biases should be           #
        # initialized to zero. All weights and biases should be stored in the      #
        # dictionary self.params, with first layer weights                         #
        # and biases using the keys 'W1' and 'b1' and second layer                 #
        # weights and biases using the keys 'W2' and 'b2'.                         #
        ############################################################################
        # *****START OF YOUR CODE (DO NOT DELETE/MODIFY THIS LINE)*****
        self.params['W1'] = weight_scale * np.random.randn(input_dim, hidden_dim)
        self.params['b1'] = np.zeros(hidden_dim)
        self.params['W2'] = weight_scale * np.random.randn(hidden_dim, num_classes)
        self.params['b2'] = np.zeros(num_classes)

        pass

        # *****END OF YOUR CODE (DO NOT DELETE/MODIFY THIS LINE)*****
        ############################################################################
        #                             END OF YOUR CODE                             #
        ############################################################################

    def loss(self, X, y=None):
        """
        Compute loss and gradient for a minibatch of data.

        Inputs:
        - X: Array of input data of shape (N, d_1, ..., d_k)
        - y: Array of labels, of shape (N,). y[i] gives the label for X[i].

        Returns:
        If y is None, then run a test-time forward pass of the model and return:
        - scores: Array of shape (N, C) giving classification scores, where
          scores[i, c] is the classification score for X[i] and class c.

        If y is not None, then run a training-time forward and backward pass and
        return a tuple of:
        - loss: Scalar value giving the loss
        - grads: Dictionary with the same keys as self.params, mapping parameter
          names to gradients of the loss with respect to those parameters.
        """
        scores = None
        ############################################################################
        # TODO: Implement the forward pass for the two-layer net, computing the    #
        # class scores for X and storing them in the scores variable.              #
        ############################################################################
        # *****START OF YOUR CODE (DO NOT DELETE/MODIFY THIS LINE)*****
        N = X.shape[0]
        
        h1, self.cache1 = affine_relu_forward(X.reshape(N, -1), self.params['W1'], self.params['b1'])
        scores, self.cache2 = affine_forward(h1, self.params['W2'], self.params['b2'])

        pass

        # *****END OF YOUR CODE (DO NOT DELETE/MODIFY THIS LINE)*****
        ############################################################################
        #                             END OF YOUR CODE                             #
        ############################################################################

        # If y is None then we are in test mode so just return scores
        if y is None:
            return scores

        loss, grads = 0, {}
        ############################################################################
        # TODO: Implement the backward pass for the two-layer net. Store the loss  #
        # in the loss variable and gradients in the grads dictionary. Compute data #
        # loss using softmax, and make sure that grads[k] holds the gradients for  #
        # self.params[k]. Don't forget to add L2 regularization!                   #
        #                                                                          #
        # NOTE: To ensure that your implementation matches ours and you pass the   #
        # automated tests, make sure that your L2 regularization includes a factor #
        # of 0.5 to simplify the expression for the gradient.                      #
        ############################################################################
        # *****START OF YOUR CODE (DO NOT DELETE/MODIFY THIS LINE)*****
        loss, dscores = softmax_loss(scores, y)
        loss += 0.5* self.reg * np.sum(self.params['W2'] * self.params['W2']) \
                + 0.5* self.reg * np.sum(self.params['W1'] * self.params['W1'])
        dh1, dw2, db2 = affine_backward(dscores, self.cache2)
        _, dw1, db1 = affine_relu_backward(dh1, self.cache1)
        grads['W1'] = dw1 + self.reg * self.params['W1']
        grads['b1'] = db1
        grads['W2'] = dw2 + self.reg * self.params['W2']
        grads['b2'] = db2
        

        pass

        # *****END OF YOUR CODE (DO NOT DELETE/MODIFY THIS LINE)*****
        ############################################################################
        #                             END OF YOUR CODE                             #
        ############################################################################

        return loss, grads


class FullyConnectedNet(object):
    """
    A fully-connected neural network with an arbitrary number of hidden layers,
    ReLU nonlinearities, and a softmax loss function. This will also implement
    dropout and batch/layer normalization as options. For a network with L layers,
    the architecture will be

    {affine - [batch/layer norm] - relu - [dropout]} x (L - 1) - affine - softmax

    where batch/layer normalization and dropout are optional, and the {...} block is
    repeated L - 1 times.

    Similar to the TwoLayerNet above, learnable parameters are stored in the
    self.params dictionary and will be learned using the Solver class.
    """

    def __init__(
        self,
        hidden_dims,
        input_dim=3 * 32 * 32,
        num_classes=10,
        dropout=1,
        normalization=None,
        reg=0.0,
        weight_scale=1e-2,
        dtype=np.float32,
        seed=None,
    ):
        """
        Initialize a new FullyConnectedNet.

        Inputs:
        - hidden_dims: A list of integers giving the size of each hidden layer.
        - input_dim: An integer giving the size of the input.
        - num_classes: An integer giving the number of classes to classify.
        - dropout: Scalar between 0 and 1 giving dropout strength. If dropout=1 then
          the network should not use dropout at all.
        - normalization: What type of normalization the network should use. Valid values
          are "batchnorm", "layernorm", or None for no normalization (the default).
        - reg: Scalar giving L2 regularization strength.
        - weight_scale: Scalar giving the standard deviation for random
          initialization of the weights.
        - dtype: A numpy datatype object; all computations will be performed using
          this datatype. float32 is faster but less accurate, so you should use
          float64 for numeric gradient checking.
        - seed: If not None, then pass this random seed to the dropout layers. This
          will make the dropout layers deteriminstic so we can gradient check the
          model.
        """
        self.normalization = normalization
        self.use_dropout = dropout != 1
        self.reg = reg
        self.num_layers = 1 + len(hidden_dims)
        self.dtype = dtype
        self.params = {}

        ############################################################################
        # TODO: Initialize the parameters of the network, storing all values in    #
        # the self.params dictionary. Store weights and biases for the first layer #
        # in W1 and b1; for the second layer use W2 and b2, etc. Weights should be #
        # initialized from a normal distribution centered at 0 with standard       #
        # deviation equal to weight_scale. Biases should be initialized to zero.   #
        #                                                                          #
        # When using batch normalization, store scale and shift parameters for the #
        # first layer in gamma1 and beta1; for the second layer use gamma2 and     #
        # beta2, etc. Scale parameters should be initialized to ones and shift     #
        # parameters should be initialized to zeros.                               #
        ############################################################################
        # *****START OF YOUR CODE (DO NOT DELETE/MODIFY THIS LINE)*****
        if self.normalization:
            for i in range(self.num_layers):
                layer = i+1
                str_w = 'W' + str(layer)
                str_b = 'b' + str(layer)
                str_gamma = 'gamma' + str(layer)
                str_beta = 'beta' + str(layer)

                if layer == 1:
                    self.params[str_w] = weight_scale * \
                        np.random.randn(input_dim, hidden_dims[i])
                    self.params[str_b] = np.zeros(hidden_dims[i])
                    
                    self.params[str_gamma] = np.ones(input_dim) #TODO 维度不对
                    self.params[str_beta] = np.zeros(input_dim)
                elif layer == self.num_layers:
                    self.params[str_w] = weight_scale * \
                        np.random.randn(hidden_dims[i-1], num_classes)
                    self.params[str_b] = np.zeros(num_classes)
                else:
                    self.params[str_w] = weight_scale * \
                        np.random.randn(hidden_dims[i-1], hidden_dims[i])
                    self.params[str_b] = np.zeros(hidden_dims[i])

                    self.params[str_gamma] = np.ones(input_dim)
                    self.params[str_beta] = np.zeros(input_dim)
        else:
            for i in range(self.num_layers):
                layer = i+1
                str_w = 'W' + str(layer)
                str_b = 'b' + str(layer)

                if layer == 1:
                    self.params[str_w] = weight_scale * \
                        np.random.randn(input_dim, hidden_dims[i])
                    self.params[str_b] = np.zeros(hidden_dims[i])
                elif layer == self.num_layers:
                    self.params[str_w] = weight_scale * \
                        np.random.randn(hidden_dims[i-1], num_classes)
                    self.params[str_b] = np.zeros(num_classes)
                else:
                    self.params[str_w] = weight_scale * \
                        np.random.randn(hidden_dims[i-1], hidden_dims[i])
                    self.params[str_b] = np.zeros(hidden_dims[i])

        pass

        # *****END OF YOUR CODE (DO NOT DELETE/MODIFY THIS LINE)*****
        ############################################################################
        #                             END OF YOUR CODE                             #
        ############################################################################

        # When using dropout we need to pass a dropout_param dictionary to each
        # dropout layer so that the layer knows the dropout probability and the mode
        # (train / test). You can pass the same dropout_param to each dropout layer.
        self.dropout_param = {}
        if self.use_dropout:
            self.dropout_param = {"mode": "train", "p": dropout}
            if seed is not None:
                self.dropout_param["seed"] = seed

        # With batch normalization we need to keep track of running means and
        # variances, so we need to pass a special bn_param object to each batch
        # normalization layer. You should pass self.bn_params[0] to the forward pass
        # of the first batch normalization layer, self.bn_params[1] to the forward
        # pass of the second batch normalization layer, etc.
        self.bn_params = []
        if self.normalization == "batchnorm":
            self.bn_params = [{"mode": "train"} for i in range(self.num_layers - 1)]
        if self.normalization == "layernorm":
            self.bn_params = [{} for i in range(self.num_layers - 1)]

        # Cast all parameters to the correct datatype
        for k, v in self.params.items():
            self.params[k] = v.astype(dtype)

    def loss(self, X, y=None):
        """
        Compute loss and gradient for the fully-connected net.

        Input / output: Same as TwoLayerNet above.
        """
        X = X.astype(self.dtype)
        mode = "test" if y is None else "train"

        # Set train/test mode for batchnorm params and dropout param since they
        # behave differently during training and testing.
        if self.use_dropout:
            self.dropout_param["mode"] = mode
        if self.normalization == "batchnorm":
            for bn_param in self.bn_params:
                bn_param["mode"] = mode
        scores = None
        ############################################################################
        # TODO: Implement the forward pass for the fully-connected net, computing  #
        # the class scores for X and storing them in the scores variable.          #
        #                                                                          #
        # When using dropout, you'll need to pass self.dropout_param to each       #
        # dropout forward pass.                                                    #
        #                                                                          #
        # When using batch normalization, you'll need to pass self.bn_params[0] to #
        # the forward pass for the first batch normalization layer, pass           #
        # self.bn_params[1] to the forward pass for the second batch normalization #
        # layer, etc.                                                              #
        ############################################################################
        # *****START OF YOUR CODE (DO NOT DELETE/MODIFY THIS LINE)*****
        N = X.shape[0]
        h={}
        self.cache = {}
        
        if self.normalization:
            for i in range(self.num_layers):
                layer = i+1
                str_w = 'W' + str(layer)
                str_b = 'b' + str(layer)
                str_gamma = 'gamma' + str(layer)
                str_beta = 'beta' + str(layer)
                str_gamma = 'gamma' + str(layer)
                str_beta = 'beta' + str(layer)
                if layer == 1:
                    h[layer], self.cache[layer] = affine_bn_relu_forward(
                        X.reshape(N, -1), self.params[str_w], self.params[str_b], self.params[str_gamma], self.params[str_beta], bn_param)
                elif layer == self.num_layers:
                    scores, self.cache[layer] = affine_forward(
                        h[layer-1], self.params[str_w], self.params[str_b])
                else:
                    h[layer], self.cache[layer] = affine_bn_relu_forward(
                        h[layer - 1], self.params[str_w], self.params[str_b], self.params[str_gamma], self.params[str_beta], bn_param)
        else:
            for i in range(self.num_layers):
                layer = i+1
                str_w = 'W' + str(layer)
                str_b = 'b' + str(layer)
                if layer == 1:
                        h[layer], self.cache[layer] = affine_relu_forward(
                            X.reshape(N, -1), self.params[str_w], self.params[str_b])
                elif layer == self.num_layers:
                    scores, self.cache[layer] = affine_forward(
                        h[layer-1], self.params[str_w], self.params[str_b])
                else:
                    h[layer], self.cache[layer] = affine_relu_forward(
                        h[layer - 1], self.params[str_w], self.params[str_b])

        pass

        # *****END OF YOUR CODE (DO NOT DELETE/MODIFY THIS LINE)*****
        ############################################################################
        #                             END OF YOUR CODE                             #
        ############################################################################

        # If test mode return early
        if mode == "test":
            return scores

        loss, grads = 0.0, {}
        ############################################################################
        # TODO: Implement the backward pass for the fully-connected net. Store the #
        # loss in the loss variable and gradients in the grads dictionary. Compute #
        # data loss using softmax, and make sure that grads[k] holds the gradients #
        # for self.params[k]. Don't forget to add L2 regularization!               #
        #                                                                          #
        # When using batch/layer normalization, you don't need to regularize the scale   #
        # and shift parameters.                                                    #
        #                                                                          #
        # NOTE: To ensure that your implementation matches ours and you pass the   #
        # automated tests, make sure that your L2 regularization includes a factor #
        # of 0.5 to simplify the expression for the gradient.                      #
        ############################################################################
        # *****START OF YOUR CODE (DO NOT DELETE/MODIFY THIS LINE)*****
        loss, dscores = softmax_loss(scores, y)
        for i in range(self.num_layers):
            str_w = 'W' + str(i+1)
            loss += 0.5*self.reg*np.sum(self.params[str_w] * self.params[str_w])

        dh = {}

        if self.normalization:
            for layer in range(self.num_layers, 0, -1):
                i = layer - 1
                str_w = 'W' + str(layer)
                str_b = 'b' + str(layer)
                str_gamma = 'gamma' + str(layer)
                str_beta = 'beta' + str(layer)
                str_gamma = 'gamma' + str(layer)
                str_beta = 'beta' + str(layer)
                if layer == self.num_layers:
                    dh[i], grads[str_w], grads[str_b] = affine_backward(
                        dscores, self.cache[layer])
                else:
                    dh[i], grads[str_w], grads[str_b], grads[str_gamma], grads[str_beta]  = affine_bn_relu_backward(
                        dh[layer], self.cache[layer])

                grads[str_w] += self.reg * self.params[str_w]
        else:
            for layer in range(self.num_layers, 0, -1):
                i = layer -1
                str_w = 'W' + str(layer)
                str_b = 'b' + str(layer)

                if layer == self.num_layers:
                    dh[i], grads[str_w], grads[str_b] = affine_backward(dscores, self.cache[layer])
                else:
                    dh[i], grads[str_w], grads[str_b] = affine_relu_backward(dh[layer], self.cache[layer])
                
                grads[str_w] += self.reg * self.params[str_w]
        pass

        # *****END OF YOUR CODE (DO NOT DELETE/MODIFY THIS LINE)*****
        ############################################################################
        #                             END OF YOUR CODE                             #
        ############################################################################

        return loss, grads


def affine_bn_relu_forward(x, w, b, gamma, beta, bn_param):
    a, fc_cache = affine_forward(x, w, b)
    b, bn_cache = batchnorm_forward(a, gamma, beta, bn_param)
    out, relu_cache = relu_forward(b)

    cache = (fc_cache, bn_cache, relu_cache)

    return out, cache

def affine_bn_relu_backward(dout, cache):
    fc_cache, bn_cache, relu_cache = cache
    db = relu_backward(dout, relu_cache)
    da, dgamma, dbeta = batchnorm_backward(db, bn_cache)
    dx, dw, db = affine_backward(da, fc_cache)
    return dx, dw, db, dgamma, dbeta
