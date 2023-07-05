// import { createRequire } from 'module';
// const require = createRequire(import.meta.url);

function loadShader(gl, type, source) {
  const shader = gl.createShader(type);

  // Send the source to the shader object
  gl.shaderSource(shader, source);
  gl.compileShader(shader);

  // See if it compiled successfully
  if (!gl.getShaderParameter(shader, gl.COMPILE_STATUS)) {
    alert(
      `An error occurred compiling the shaders: ${gl.getShaderInfoLog(shader)}`
    );
    gl.deleteShader(shader);
    return null;
  }

  return shader;
}

const vert_glsl = `#version 300 es
void main() {
  gl_Position = vec4(0, 0, 0, 1);
  gl_PointSize = 50.0;
}`

const frag_glsl = `#version 300 es
precision highp float;
out vec4 color;
void main() {
  color = vec4(1, 0, 1, 1);
}`

function initShaders(gl) {
  const vertexShader = loadShader(gl, gl.VERTEX_SHADER, vert_glsl);
  const fragmentShader = loadShader(gl, gl.FRAGMENT_SHADER, frag_glsl);
  const shaderProgram = gl.createProgram();
  gl.attachShader(shaderProgram, vertexShader);
  gl.attachShader(shaderProgram, fragmentShader);
  gl.linkProgram(shaderProgram);

  // If creating the shader program failed, alert

  if (!gl.getProgramParameter(shaderProgram, gl.LINK_STATUS)) {
    alert(
      `Unable to initialize the shader program: ${gl.getProgramInfoLog(
        shaderProgram
      )}`
    );
    return null;
  }


  return shaderProgram;
}

export { initShaders }