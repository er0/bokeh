import numpy as np
from ..objects import ServerDataSource

try:
    import scipy
    import scipy.misc
except ImportError as e:
    print(e)


def source(**kwargs):
  kwargs['transform'] = {'resample':'heatmap'}
  kwargs['data'] = {'x': [0], 
                                'y': [0],
                                'global_x_range' : [0, 10],
                                'global_y_range' : [0, 10],
                                'global_offset_x' : [0],
                                'global_offset_y' : [0],
                                'dw' : [10], 
                                'dh' : [10], 
                                'palette': ["Spectral-11"]
                            }
  return ServerDataSource(**kwargs)


def downsample(image, image_x_axis, image_y_axis,
               x_bounds, y_bounds, x_resolution, y_resolution):
    x_resolution, y_resolution = int(round(x_resolution)), int(round(y_resolution))
    x_bounds = [x_bounds.start, x_bounds.end]
    y_bounds = [y_bounds.start, y_bounds.end]
    x_bounds = np.searchsorted(image_x_axis, x_bounds)
    y_bounds = np.searchsorted(image_y_axis, y_bounds)
    #y_bounds = image.shape[0] + 1 - y_bounds[::-1]
    subset = image[y_bounds[0]:y_bounds[1],
                   x_bounds[0]:x_bounds[1]]
    x_downsample_factor = max(round(subset.shape[1] / x_resolution / 3.), 1)
    y_downsample_factor = max(round(subset.shape[0] / y_resolution / 3.), 1)
    subset = subset[::x_downsample_factor, ::y_downsample_factor]
    image = scipy.misc.imresize(subset, (x_resolution, y_resolution),
                        interp='nearest')
    bounds = image_x_axis[x_bounds[0]:x_bounds[1]]
    dw = np.max(bounds) - np.min(bounds)
    bounds = image_y_axis[y_bounds[0]:y_bounds[1]]
    dh = np.max(bounds) - np.min(bounds)
    return {'data': image,
            'offset_x': image_x_axis[x_bounds[0]],
            'offset_y': image_y_axis[y_bounds[0]],
            'dw': dw,
            'dh': dh,
            'subset': subset,
    }
