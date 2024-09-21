"""Methods for working with Points objects.
"""

import warnings
warnings.filterwarnings("ignore", category=FutureWarning)

import numpy as np
from genepy3d.obj.points import Points   

def to_Point_3_CGAL(pnts):
    """Return the Points object as a list of Point_3 objects in CGAL.

    Args:
        pnts (Points): Points object.
                            
    Returns:
        A list of CGAL.Point_3 objects.
    
    """
    
    from CGAL.CGAL_Kernel import Point_3
    
     #import CGAL? needs to be done from the caller, TODO: test that it's done
    return [Point_3(pnts.coors[i,0],pnts.coors[i,1],pnts.coors[i,2]) for i in range(len(pnts.coors))]

def to_Point_set_3_CGAL(pnts):
    """Convert Points object to Point_set_3 object in CGAL.

    Args:
        pnts (Points): Points object.

    Returns:
        Point_set_3 object in CGAL.

    """

    from CGAL.CGAL_Kernel import Point_3
    from CGAL.CGAL_Point_set_3 import Point_set_3

    pntset = Point_set_3()

    # Insertions
    for i in range(pnts.size):
        idx = pntset.insert(Point_3(pnts.coors[i,0],pnts.coors[i,1],pnts.coors[i,2]))

    return pntset


def process(pnts,removed_percentage = 5.0,nb_neighbors = 24, smooth=True):
    """Process the points cloud by outlier removal and smoothing.

    Details can be see here [1].

    Args:
        pnts (Points): Points object.
        removed_percentage (float): % of outlier removal.
        nb_neighbors (int): number of neighboring points used in outlier removal and smoothing algorithms.
        smooth (bool): if True, then smooth the points cloud.

    Returns:
        A processed Points object.

    References:
        ..  [1] https://doc.cgal.org/4.3/Point_set_processing_3/index.html

    Examples:
        ..  code-block:: python

            import numpy as np
            from sklearn.datasets import make_blobs
            from genepy3d.obj.points import Points
            from genepy3d_gpl.obj import points
            import matplotlib.pyplot as plt

            # Generate random 3D points
            coors, _ = make_blobs(n_features=3, centers = [(0, 0, 0)], n_samples=500, cluster_std=3.)
            pnts = Points(coors)

            # Remove outliers (20% of points)
            pnts_processed = points.process(pnts,removed_percentage=20,smooth=False)

            # Plot
            fig = plt.figure()
            ax = fig.add_subplot(111,projection='3d')
            pnts.plot(ax,point_args={'alpha':0.2})
            pnts_processed.plot(ax,point_args={'color':"r",'s':3})



    """
    
    from CGAL.CGAL_Point_set_processing_3 import remove_outliers,jet_smooth_point_set

    pointsCgal= to_Point_set_3_CGAL(pnts)
     
    if removed_percentage:
        new_size=remove_outliers(pointsCgal, nb_neighbors, removed_percentage)
        # pointsCgal=pointsCgal[0:new_size]
        pointsCgal.collect_garbage()
        
    if smooth:
        jet_smooth_point_set(pointsCgal,nb_neighbors)

    
    return Points(np.array([[p.x(),p.y(),p.z()] for p in pointsCgal.points()]))
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
