%================================== SE3 ==================================
%
%  class SE3
%
%  g = SE3(d, theta)
%
%
%  A Matlab class implementation of SE(2) [Special Euclidean 2-space].
%  Allows for the operations written down as math equations to be
%  reproduced in Matlab as code.  At least that's the idea.  It's about
%  as close as one can get to the math.
%
%================================== SE3 ==================================
classdef SE3 < handle


properties (Access = protected)
  M;            % Internal implementation is homogeneous.
end

%
%========================= Public Member Methods =========================
%

methods

  %-------------------------------- SE3 --------------------------------
  %
  %  Constructor for the class.  Expects translation vector and rotation
  %  angle.  If both missing, then initialize as identity.
  %
  function g = SE3(d, R)

  if (nargin == 0)
    g.M = eye(4);
  else
    g.M = [R, d; 0 0 0 1];
  end

  end


  %------------------------------- inv -------------------------------
  %
  %  Returns the inverse of the element g.  Can invoke in two ways:
  %
  %    g.inv();
  %
  %  or
  %
  %    inv(g);
  %
  %
  function invg = inv(g)

  invg = SE3();       % Create the return element as identity element.
  invM = inv(g.M);        % Compute inverse of matrix.
  invg.M = invM;      % Set matrix of newly created element to inverse.

  end

  %------------------------------ times ------------------------------
  %
  %  This function is the operator overload that implements the left
  %  action of g on the point p.
  %
  %  Can be invoked in the following equivalent ways:
  %
  %  >> p2 = g .* p;
  %
  %  >> p2 = times(g, p);
  %  
  %  >> p2 = g.times(p);
  %
  function p2 = times(g, el)

  p2 = g.leftact(el);

  end
  
  %------------------------------ mtimes -----------------------------
  %
  %  Computes and returns the product of g1 with g2.
  %
  %  Can be invoked in the following equivalent ways:  
  %
  %  >> g3 = g1 * g2;
  %
  %  >> g3 = g1.mtimes(g2);
  %
  %  >> g3 = mtimes(g1, g2);
  %
  function g3 = mtimes(g1, g2)

  g3 = SE3();           % Initialize return element as identity.

  Mat = g1.M * g2.M;

  g3.M = Mat;    % Set the return element matrix to product.

  end

  %----------------------------- leftact -----------------------------
  %
  %  g.leftact(p)     --> same as g . p
  %
  %               with p a 2x1 specifying point coordinates.
  %
  %  g.leftact(v)     --> same as g . v
  %
  %               with v a 3x1 specifying a velocity.
  %               This applies to pure translational velocities in
  %               homogeneous form, or to SE3 velocities in vector forn.
  %
  %  This function takes a change of coordinates and a point/velocity,
  %  and returns the transformation of that point/velocity under the
  %  change of coordinates.  
  %  
  %  Alternatively, one can think of the change of coordinates as a 
  %  transformation of the point to somewhere else, e.g., a displacement 
  %  of the point.  It all depends on one's perspective of the 
  %  operation/situation.
  %
  function x2 = leftact(g, x)

  if ( (size(x,1) == 3) && (size(x,2) == 1) )
   x = [x;1];
   x3 = g.M * x;
   x2 = [x3(1);x3(2);x3(3)];
  elseif ( (size(x,1) == 4) && (size(x,2) == 1) )
   x2 = g.M * x;
  elseif ( (size(x,1) == 4) && (size(x,2) == 4) )
   x2 = g.M * x;
  end
  end


  %
  %--------------------------- getTranslation --------------------------
  %
  %  Get the translation vector of the frame/object.
  %
  %
  function T = getTranslation(g)

  T = g.M(1:1:3, 4);

  end

  %------------------------- getRotationMatrix -------------------------
  %
  %  Get the rotation or orientation of the frame/object.
  %
  %
  function R = getRotationMatrix(g)

  R = g.M(1:1:3,1:1:3);

  end

end




  %-------------------------------- RotX -------------------------------
  %
  %  Takes an angle and generates rotation matrix about that angle,
  %  with respect to x-axis.
  %
  function Rmat = RotX(ang)

  Rmat = [1,0,0;0,cos(ang),-sin(ang);0,sin(ang),cos(ang)];
  end

  %-------------------------------- RotY -------------------------------
  %
  %  Takes an angle and generates rotation matrix about that angle.
  %  with respect to y-axis.
  %
  function Rmat = RotY(ang)

  Rmat = [cos(ang),0,sin(ang);0,1,0;-sin(ang),0,cos(ang)];
  end

  %-------------------------------- RotZ -------------------------------
  %
  %  Takes an angle and generates rotation matrix about that angle.
  %  with respect to z-axis.
  %
  function Rmat = RotZ(ang)
      
  Rmat = [cos(ang),-sin(ang),0;sin(ang),cos(ang),0;0,0,1];
  end

  %---------------------------- EulerXYZtoR ----------------------------
  %
  %  Generates a rotation matrix given the x-y-z Euler angle convention.
  %
  function Rmat = EulerXYZtoR(thX, thY, thZ)

  Rmat = RotX(thX) * RotY(thY) * RotZ(thZ);

  end

  %---------------------------- RtoEulerXYZ ----------------------------
  %
  %  Generates a rotation matrix given the x-y-z Euler angle convention.
  %
  function [Rx, Ry, Rz] = RtoEulerXYZ(Rmat)

  Ry = -asin(Rmat(3,1));
  Rx = atan2(Rmat(3,2),Rmat(3,3));
  Rz = atan2(Rmat(2,1),Rmat(1,1));
  
  end


end


end
