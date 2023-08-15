import { initBuffers } from "./init-buffers.js";
import { initShaders } from "./init-shaders.js";
import { drawScene } from "./draw-scene.js";
import { initCamera } from "./camera.js";

function main() {
  const canvas = document.querySelector("#glcanvas");
  // Initialize the GL context
  const gl = canvas.getContext("webgl2");

  // Only continue if WebGL is available and working
  if (gl === null) {
    alert(
      "Unable to initialize WebGL. Your browser or machine may not support it."
    );
    return;
  }

  const camera = initCamera(gl);
  const buffers = initBuffers(gl);
  const shaders = initShaders(gl);
  // // Draw the scene
  // drawScene(gl, programInfo, buffers);
  const uniforms = {

  }
  draw(gl, shaders, uniforms)
}

function draw(gl, shaders, buffers) {
  gl.clearColor(0.0, 0.0, 0.0, 1.0); // Clear to black, fully opaque
  gl.clearDepth(1.0); // Clear everything
  gl.enable(gl.DEPTH_TEST); // Enable depth testing
  gl.depthFunc(gl.LEQUAL); // Near things obscure far things
  // Clear the canvas before we start drawing on it.
  gl.clear(gl.COLOR_BUFFER_BIT | gl.DEPTH_BUFFER_BIT);
  

  // let line = createLine(gl)

  // // Tell WebGL how to pull out the positions from the position
  // // buffer into the vertexPosition attribute.
  // setPositionAttribute(gl, buffers, programInfo);

  // setColorAttribute(gl, buffers, programInfo);

  // setLineAttribute(gl, buffers, programInfo);

  // // Tell WebGL to use our program when drawing
  // gl.useProgram(programInfo.program);

  // // Set the shader uniforms
  // gl.uniform3fv(
  //   programInfo.uniformLocations.diffuse,
  //   [1.0, 0.0, 1.0]
  // );
  // gl.uniform1fv(
  //   programInfo.uniformLocations.opacity,
  //   [1.0]
  // )
  // gl.uniform1fv(
  //   programInfo.uniformLocations.thickness,
  //   [1.0]
  // )
  // gl.uniformMatrix4fv(
  //   programInfo.uniformLocations.modelViewMatrix,
  //   false,
  //   modelViewMatrix
  // );

  gl.useProgram(shaders);
  {
    const offset = 0;
    const vertexCount = 4;
    gl.drawArrays(gl.TRIANGLE_STRIP, offset, vertexCount);
  }

}

await main();