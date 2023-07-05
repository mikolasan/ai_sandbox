import createLine from './gl-line-3d.js'

function drawScene(gl, programInfo, buffers) {
  gl.clearColor(0.0, 0.0, 0.0, 1.0); // Clear to black, fully opaque
  gl.clearDepth(1.0); // Clear everything
  gl.enable(gl.DEPTH_TEST); // Enable depth testing
  gl.depthFunc(gl.LEQUAL); // Near things obscure far things

  // Clear the canvas before we start drawing on it.

  gl.clear(gl.COLOR_BUFFER_BIT | gl.DEPTH_BUFFER_BIT);

  
  let line = createLine(gl)

  // // Tell WebGL how to pull out the positions from the position
  // // buffer into the vertexPosition attribute.
  // setPositionAttribute(gl, buffers, programInfo);

  // setColorAttribute(gl, buffers, programInfo);

  // setLineAttribute(gl, buffers, programInfo);

  // Tell WebGL to use our program when drawing
  gl.useProgram(programInfo.program);

  // Set the shader uniforms
  gl.uniform3fv(
    programInfo.uniformLocations.diffuse,
    [1.0, 0.0, 1.0]
  );
  gl.uniform1fv(
    programInfo.uniformLocations.opacity,
    [1.0]
  )
  gl.uniform1fv(
    programInfo.uniformLocations.thickness,
    [1.0]
  )
  // gl.uniformMatrix4fv(
  //   programInfo.uniformLocations.modelViewMatrix,
  //   false,
  //   modelViewMatrix
  // );

  // {
  //   const offset = 0;
  //   const vertexCount = 4;
  //   gl.drawArrays(gl.TRIANGLE_STRIP, offset, vertexCount);
  // }

  gl.drawArrays(gl.POINTS, 0, 1) // draw 1 point

}

// function setLineAttribute(gl, buffers, programInfo) {
//   const boxPath = [[0, 0], [1, 0], [1, 1], [0, 1]];
//   gl.vertexAttribPointer
// }

// Tell WebGL how to pull out the positions from the position
// buffer into the vertexPosition attribute.
function setPositionAttribute(gl, buffers, programInfo) {
  const numComponents = 2; // pull out 2 values per iteration
  const type = gl.FLOAT; // the data in the buffer is 32bit floats
  const normalize = false; // don't normalize
  const stride = 0; // how many bytes to get from one set of values to the next
  // 0 = use type and numComponents above
  const offset = 0; // how many bytes inside the buffer to start from
  gl.bindBuffer(gl.ARRAY_BUFFER, buffers.position);
  gl.vertexAttribPointer(
    programInfo.attribLocations.vertexPosition,
    numComponents,
    type,
    normalize,
    stride,
    offset
  );
  gl.enableVertexAttribArray(programInfo.attribLocations.vertexPosition);
}

// Tell WebGL how to pull out the colors from the color buffer
// into the vertexColor attribute.
function setColorAttribute(gl, buffers, programInfo) {
  const numComponents = 4;
  const type = gl.FLOAT;
  const normalize = false;
  const stride = 0;
  const offset = 0;
  gl.bindBuffer(gl.ARRAY_BUFFER, buffers.color);
  gl.vertexAttribPointer(
    programInfo.attribLocations.vertexColor,
    numComponents,
    type,
    normalize,
    stride,
    offset
  );
  gl.enableVertexAttribArray(programInfo.attribLocations.vertexColor);
}

export { drawScene };
