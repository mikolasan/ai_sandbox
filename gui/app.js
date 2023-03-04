import { calc_angle, calc_distance } from '../ann/world.js';
import { findPath } from '../ann/astar.js';
import * as PIXI from 'pixi.js';

PIXI.Graphics.prototype.drawDashedPath = function(path, x, y, dash, gap, offsetPercentage){
  var i;
  var p1;
  var p2;
  var dashLeft = 0;
  var gapLeft = 0;
  if(offsetPercentage>0){
    var progressOffset = (dash+gap)*offsetPercentage;
    if(progressOffset < dash) dashLeft = dash-progressOffset;
    else gapLeft = gap-(progressOffset-dash);
  }
  for(i = 0; i<path.length-1; i++){
    p1 = path[i];
    p2 = path[i+1];
    var dx = p2.x-p1.x;
    var dy = p2.y-p1.y;
    var len = Math.sqrt(dx*dx+dy*dy);
    var normal = {x:dx/len, y:dy/len};
    var progressOnLine = 0;
    this.moveTo(x+p1.x+gapLeft*normal.x, y+p1.y+gapLeft*normal.y);
    while(progressOnLine<=len){
      progressOnLine+=gapLeft;
      if(dashLeft > 0) progressOnLine += dashLeft;
      else progressOnLine+= dash;
      if(progressOnLine>len){
        dashLeft = progressOnLine-len;
        progressOnLine = len;
      }else{
        dashLeft = 0;
      }
      this.lineTo(x+p1.x+progressOnLine*normal.x, y+p1.y+progressOnLine*normal.y);
      progressOnLine+= gap;
      if(progressOnLine>len && dashLeft == 0){
        gapLeft = progressOnLine-len;
      }else{
        gapLeft = 0;
        this.moveTo(x+p1.x+progressOnLine*normal.x, y+p1.y+progressOnLine*normal.y);
      }
    }
  }
}

// Create the application helper and add its render target to the page
let app = new PIXI.Application({
  width: 800,
  height: 640,
  background: '#1099bb',
});
let root = document.getElementsByClassName("pixi-canvas");
if (root.length > 0) {
  root[0].appendChild(app.view);
} else {
  console.error(`Where's "pixi-canvas"?`)
}


const container = new PIXI.Container();
app.stage.addChild(container);

const thickness = 2;
const line_color = 0x145252;

const y_cell = 64;
const y_lines = 5;
const width = y_cell * y_lines;
let template = new PIXI.Graphics();
for (let y = 0; y <= y_lines; ++y) {
  template
  .lineStyle(thickness, line_color)
  .moveTo(0, y * y_cell)
  .lineTo(width, y * y_cell);
}

const x_cell = 64;
const x_lines = 5;
const height = x_cell * x_lines;
for (let x = 0; x <= x_lines; ++x) {
  template
  .lineStyle(thickness, line_color)
  .moveTo(x * x_cell, 0)
  .lineTo(x * x_cell, height);
}

// // Create a 5x5 grid of bunnies
// for (let i = 0; i < 25; i++) {
//   const bunny = new PIXI.Sprite(texture);
//   bunny.anchor.set(0.5);
//   bunny.x = (i % 5) * 40;
//   bunny.y = Math.floor(i / 5) * 40;
//   container.addChild(bunny);
// }

container.addChild(template);

// Move container to the center
container.x = app.screen.width / 2;
container.y = app.screen.height / 2;

// Center bunny sprite in local container coordinates
container.pivot.x = container.width / 2;
container.pivot.y = container.height / 2;

// Create the sprite and add it to the stage
let robot = PIXI.Sprite.from('robot-64.png');
robot.x = 2 * x_cell;
robot.y = 2 * y_cell;
container.addChild(robot);

// // Add a ticker callback to move the sprite back and forth
// let elapsed = 0.0;
// app.ticker.add((delta) => {
//   elapsed += delta;
//   sprite.x =  100.0 + Math.cos(elapsed/50.0) * 100.0;
// });


const player = PIXI.Sprite.from("aim.png");
player.anchor.set(0.5);
player.x = app.screen.width / 2 - robot.x;
player.y = app.screen.height / 2 - robot.y;

app.stage.addChild(player);

let hint = new PIXI.Graphics();
hint
.lineStyle(thickness, 0x000000)
.moveTo(player.x, player.y)
.lineTo(player.x + robot.x, player.y + robot.y);
app.stage.addChild(hint);

const basicText = new PIXI.Text('???');
basicText.x = 50;
basicText.y = 100;

app.stage.addChild(basicText);

// mouse interactions
app.stage.hitArea = app.screen;
app.stage.interactive = true;
app.stage.on('mousemove', function(e) {
  let pos = e.data.global;
  player.x = pos.x - 10;
  player.y = pos.y - 10;

  const [x1, y1, x2, y2] = [player.x, player.y, app.screen.width / 2, app.screen.height / 2]
  hint.clear();
  hint
  .lineStyle(thickness, 0xafdf70)
  .moveTo(x1, y1)
  .lineTo(x2, y2);

  let a = calc_angle(x1, y1, x2, y2);
  let d = calc_distance(x1, y1, x2, y2);
  basicText.text = `${a * 180 / Math.PI} - ${d}`
})


var path = [];
path.push({x:-50, y:-50});
path.push({x:-50, y:50});
path.push({x:50, y:50});


var body = new PIXI.Graphics();
body.x = 200;
body.y = 100;
app.stage.addChild(body);

let elapsed = 0.0
app.ticker.add((delta) => {
  body.clear();
  body.lineStyle(2, 0xFFFFFF);
  
  elapsed += delta / 50;
  if (elapsed > 1.0) {
    elapsed -= 1.0;
  }
  body.drawDashedPath(path, 0, 0, 10, 5, elapsed);
})
