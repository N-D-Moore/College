class interpolation:

    def linear_interpolation(self, pt1, pt2, unknown):
        """Computes the linear interpolation for the unknown values using pt1 and pt2
        take as input
        pt1: known point pt1 and f(pt1) or intensity value
        pt2: known point pt2 and f(pt2) or intensity value
        unknown: take and unknown location
        return the f(unknown) or intentity at unknown"""

        # Write your code for linear interpolation here

        #(((x2-x)*(y2-y))/((x2-x1)*(y2-y1)))*Q11 + (((x-x1)*(y2-y))/((x2-x1)*(y2-y1)))*Q21
        top1 = (pt2[0]-unknown[0])*((unknown[1]+1)-unknown[1])
        bottom1 = (pt2[0]-pt1[0])*((unknown[1]+1)-(unknown[1]-1))
        left = top1/bottom1*pt1[2]
        top2 = (unknown[0]-pt1[0])*((unknown[1]+1)-unknown[1])
        bottom2 = (pt2[0]-pt1[0])*((unknown[1]+1)-(unknown[1]-1))
        right = top2/bottom2*pt2[2]
        
        temp = left+right

        return temp

    def bilinear_interpolation(self, pt1, pt2, pt3, pt4, unknown):
        """Computes the linear interpolation for the unknown values using pt1 and pt2
        take as input
        pt1: known point pt1 and f(pt1) or intensity value
        pt2: known point pt2 and f(pt2) or intensity value
        pt1: known point pt3 and f(pt3) or intensity value
        pt2: known point pt4 and f(pt4) or intensity value
        unknown: take and unknown location
        return the f(unknown) or intensity at unknown"""

        # Write your code for bilinear interpolation here
        # May be you can reuse or call linear interpolation method to compute this task

        Q1 = interpolation.linear_interpolation(self,pt1, pt2, unknown)
        Q2 = interpolation.linear_interpolation(self,pt3, pt4, unknown)

        temp = Q1+Q2

        return round(temp)
