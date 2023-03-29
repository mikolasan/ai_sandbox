import * as THREE from 'https://unpkg.com/three/build/three.module.js';

const fov = 75;
const aspect = window.innerWidth / window.innerHeight;
const near = 0.1;
const far = 1000;
const camera = new THREE.PerspectiveCamera(fov, aspect, near, far);
// camera.position.z = 5;
camera.position.set( -20, 20, 50 );
camera.lookAt( 10, 2, 0 );
camera.position.set(0, 20, 30 );


const scene = new THREE.Scene();
scene.background = new THREE.Color( 0xe0e0e0 );
// scene.fog = new THREE.Fog( 0xe0e0e0, 20, 100 );

// lights
const hemiLight = new THREE.HemisphereLight( 0x00ffff, 0x440444 );
hemiLight.position.set( 3, 2, 0 );
scene.add( hemiLight );

const dirLight = new THREE.DirectionalLight( 0xffff0f );
dirLight.position.set( 5, 5, 10 );
scene.add( dirLight );

const mesh = new THREE.Mesh( new THREE.PlaneGeometry( 2000, 2000 ), new THREE.MeshPhongMaterial( { color: 0x999999, depthWrite: false } ) );
mesh.rotation.x = - Math.PI / 2;
scene.add( mesh );

const grid = new THREE.GridHelper( 200, 40, 0x000000, 0x000000 );
grid.material.opacity = 0.2;
grid.material.transparent = true;
scene.add( grid );

const canvas = document.createElement( 'canvas' );
canvas.width = 128;
canvas.height = 128;

const context = canvas.getContext( '2d' );
const gradient = context.createRadialGradient( canvas.width / 2, canvas.height / 2, 0, canvas.width / 2, canvas.height / 2, canvas.width / 2 );
gradient.addColorStop( 0.1, 'rgba(210,210,210,1)' );
gradient.addColorStop( 1, 'rgba(255,255,255,1)' );

context.fillStyle = gradient;
context.fillRect( 0, 0, canvas.width, canvas.height );

const shadowTexture = new THREE.CanvasTexture( canvas );

const shadowMaterial = new THREE.MeshBasicMaterial( { map: shadowTexture } );
// const shadowGeo = new THREE.PlaneGeometry( 30, 30, 1, 1 );

// box
const geometry = new THREE.BoxGeometry( 5, 5, 5 );
const material = new THREE.MeshBasicMaterial( { color: 0x00ff00 } );

const color = new THREE.Color();
const positions = geometry.attributes.position;
const colors = geometry.attributes.color;
const count = geometry.attributes.position.count;
const radius = 200;
for ( let i = 0; i < count; i ++ ) {
  color.setHSL( ( positions.getY( i ) / radius + 1 ) / 2, 1.0, 0.5 );
  // colors.setXYZ( i, color.r, color.g, color.b );
}

// const material = new THREE.MeshPhongMaterial( {
//   color: 0xffffff,
//   flatShading: true,
//   vertexColors: true,
//   shininess: 0
// } );

const wireframeMaterial = new THREE.MeshBasicMaterial( {
  color: 0x000000,
  wireframe: true,
  transparent: true
} );

const cube = new THREE.Mesh(geometry, shadowMaterial);
scene.add( cube );

const wireframe = new THREE.Mesh(geometry, wireframeMaterial);
cube.add( wireframe );




const renderer = new THREE.WebGLRenderer( { antialias: true } );
renderer.setPixelRatio( window.devicePixelRatio );
renderer.setSize(window.innerWidth, window.innerHeight);
renderer.outputEncoding = THREE.sRGBEncoding;
document.body.appendChild(renderer.domElement);

let mouseX = 0, mouseY = 0;
let windowHalfX = window.innerWidth / 2;
let windowHalfY = window.innerHeight / 2;
let last_timestamp = 0;

let w = 0.1 * 360 / (2 * Math.PI)
let r = 0.2
let alpha = -0.2
let t_max = - w / alpha
let t = 0
console.log("t_max", t_max)

function animate(timestamp) {
  const dt = timestamp - last_timestamp;
  last_timestamp = timestamp;
  // console.log(t); // 16
  t += dt / 100;
  if (t <= t_max) {
    // console.log(cube.position.x, dt, x0 + v * t)
    let theta = w * t + 0.5 * alpha * t * t;
    cube.position.x = theta * r
    // cube.rotation.x += 0.01;
    // cube.rotation.y += 0.01;

  }
  
  // camera.position.x += ( mouseX - camera.position.x ) * 0.05;
  // camera.position.y += ( - mouseY - camera.position.y ) * 0.05;
  
  // camera.lookAt( scene.position );
  // camera.lookAt( 0, 2, 0 );
  
  renderer.render( scene, camera );
  
  requestAnimationFrame( animate );
}



function onWindowResize() {
  windowHalfX = window.innerWidth / 2;
  windowHalfY = window.innerHeight / 2;

  camera.aspect = window.innerWidth / window.innerHeight;
  camera.updateProjectionMatrix();
  renderer.setSize( window.innerWidth, window.innerHeight );
}

function onDocumentMouseMove( event ) {
  mouseX = ( event.clientX - windowHalfX );
  mouseY = ( event.clientY - windowHalfY );
}

window.addEventListener( 'resize', onWindowResize );
document.addEventListener( 'mousemove', onDocumentMouseMove );
window.requestAnimationFrame( animate );