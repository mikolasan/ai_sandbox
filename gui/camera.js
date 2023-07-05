import mat4 from 'gl-mat4';

function initCamera(gl) {
  // Create a perspective matrix, a special matrix that is
  // used to simulate the distortion of perspective in a camera.
  // Our field of view is 45 degrees, with a width/height
  // ratio that matches the display size of the canvas
  // and we only want to see objects between 0.1 units
  // and 100 units away from the camera.

  const fieldOfView = (45 * Math.PI) / 180; // in radians
  const aspect = gl.canvas.clientWidth / gl.canvas.clientHeight;
  const zNear = 0.1;
  const zFar = 100.0;
  const projectionMatrix = mat4.create();

  // note: glmatrix.js always has the first argument
  // as the destination to receive the result.
  mat4.perspective(projectionMatrix, fieldOfView, aspect, zNear, zFar);


  
  // Set the drawing position to the "identity" point, which is
  // the center of the scene.
  const modelViewMatrix = mat4.create();

  let projection = mat4.create()
  let identity = mat4.create()
  let rotation = mat4.create()
  let left = mat4.create()
  let leftRotation = mat4.create()
  let view = mat4.create()

  mat4.translate(view, view, [0.0, 0.0, -3])
  mat4.translate(left, left, [-0.25, 0.25, 0.0])
  mat4.scale(left, left, [0.5, 0.5, 0.5])
  mat4.scale(rotation, rotation, [0.75, 0.75, 0.75])
}

export { initCamera }