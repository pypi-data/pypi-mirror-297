"""Methods for working with Curve objects.
"""

import warnings
warnings.filterwarnings("ignore", category=FutureWarning)

import numpy as np
from genepy3d.obj.points import Points

def intersect(c1, c2):
    """Intersection between two curves.
    
    Args:
        c1 (Curve): curve object.
        c2 (Curve): curve object.
    
    Returns:
        list of intersected points.

    Examples:
        ..  code-block:: python

            import numpy as np
            from genepy3d.obj.curves import Curve
            from genepy3d_gpl.obj import curves
            import matplotlib.pyplot as plt

            # Create two dummy curves
            crv1 = Curve(([0.,1.,2.],[0.,1.,2.],[0.,0.,0.]))
            crv2 = Curve(([1.5,1.5,1.5],[0.,1.,2.],[0.,0.,0.]))

            # Check intersection
            pnts = curves.intersect(crv1,crv2)

            # Plot curves and intersected points
            fig = plt.figure()
            ax = fig.add_subplot(111,projection='3d')
            crv1.plot(ax,show_root=False);
            crv2.plot(ax,show_root=False);
            pnts.plot(ax);
    
    """
    
    from CGAL.CGAL_Kernel import Point_3, Segment_3
    from CGAL.CGAL_AABB_tree import AABB_tree_Segment_3_soup
    
    plst = []
    
    # create a list of segments from c1
    segments = []
    for i in range(len(c1.coors)-1):
        p1 = Point_3(c1.coors[i][0],c1.coors[i][1],c1.coors[i][2])
        p2 = Point_3(c1.coors[i+1][0],c1.coors[i+1][1],c1.coors[i+1][2])
        segment = Segment_3(p1,p2)
        segments.append(segment)
        
    # initialize AABB tree search
    tree = AABB_tree_Segment_3_soup(segments)
    
    # searching intersection between each c2 segment and c1.
    for i in range(len(c2.coors)-1):
        p1 = Point_3(c2.coors[i][0],c2.coors[i][1],c2.coors[i][2])
        p2 = Point_3(c2.coors[i+1][0],c2.coors[i+1][1],c2.coors[i+1][2])
        segment_query = Segment_3(p1,p2)
        
        if tree.do_intersect(segment_query):
            intersections = []
            tree.all_intersections(segment_query,intersections)
            for inter in intersections:
                p = inter[0].get_Point_3()
                plst.append([p.x(),p.y(),p.z()])
                
    return Points(np.array(plst))
    
    
        
        
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    

    
    


        
        