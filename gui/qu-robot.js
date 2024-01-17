import * as PIXI from 'pixi.js';
import axios from 'axios';

import { 
  x_cell, 
  y_cell, 
} from '../ann/world.js';


const final_position = [0, 0];
let aim_update_time = 0
const aim_update_delay = 60;

// Create the application helper and add its render target to the page
let app = new PIXI.Application({
  width: 800,
  height: 640,
  background: '#F4F3EE',
});
let root = document.getElementsByClassName("pixi-canvas");
if (root.length > 0) {
  root[0].appendChild(app.view);
} else {
  console.error(`Where's "pixi-canvas"?`)
}

const create_world = function(container, grid_world) {
  const x_lines = grid_world.length;
  const y_lines = grid_world[0].length;
  for (let y = 0; y < y_lines; y++) {
    for (let x = 0; x < x_lines; x++) {
      const state = grid_world[x][y];
      if (state == 'M') {
        let wall = PIXI.Sprite.from('mountains.png');
        wall.x = x * x_cell;
        wall.y = y * y_cell;
        container.addChild(wall);
      } else if (state == 'F') {
        let free = PIXI.Sprite.from('snow.png');
        free.x = x * x_cell;
        free.y = y * y_cell;
        container.addChild(free);
      } else if (state == 'H') {
        let hole = PIXI.Sprite.from('waves.png');
        hole.x = x * x_cell;
        hole.y = y * y_cell;
        container.addChild(hole);
      } else if (state == 'G') {
        let goal = PIXI.Sprite.from('igloo.png');
        goal.x = x * x_cell;
        goal.y = y * y_cell;
        container.addChild(goal);
      }
    }
  }

  const thickness = 2;
  const line_color = 0x145252;

  const width = y_cell * y_lines;
  let template = new PIXI.Graphics();
  for (let y = 0; y <= y_lines; ++y) {
    template
    .lineStyle(thickness, line_color)
    .moveTo(0, y * y_cell)
    .lineTo(width, y * y_cell);
  }

  const height = x_cell * x_lines;
  for (let x = 0; x <= x_lines; ++x) {
    template
    .lineStyle(thickness, line_color)
    .moveTo(x * x_cell, 0)
    .lineTo(x * x_cell, height);
  }

  container.addChild(template);

}

const response = await axios.get("http://localhost:8080/env");
const grid_world = response.data.grid_world;

const container = new PIXI.Container();
app.stage.addChild(container);
create_world(container, grid_world);

// Move container to the center
container.x = app.screen.width / 2;
container.y = app.screen.height / 2;

// Center bunny sprite in local container coordinates
container.pivot.x = container.width / 2;
container.pivot.y = container.height / 2;
const container_left = app.screen.width / 2 - container.width / 2;
const container_top = app.screen.height / 2 - container.height / 2;
// console.log(container_left, container_top)



// Create the sprite and add it to the stage
const robot = PIXI.Sprite.from('dinosaur.png');
container.addChild(robot);

const move_robot = function(robot_position) {
  robot.x = robot_position[0] * x_cell;
  robot.y = robot_position[1] * y_cell;
}

const label1 = new PIXI.Text('???');
label1.x = 50;
label1.y = 10;
app.stage.addChild(label1);

const label2 = new PIXI.Text('???');
label2.x = 150;
label2.y = 10;
app.stage.addChild(label2);

move_robot(response.data.loc);
const draw_current_state = function(response) {
  const meta_state = response.data.meta_state
  label1.text = `~ ${meta_state[3]} ~\n${meta_state[1]} ${meta_state[0]} ${meta_state[2]}\n~ ${meta_state[4]} ~`;
  label2.text = response.data.action_prob.join(" , ")
}

draw_current_state(response);

// step button
const button = new PIXI.Container();
button.x = 50;
button.y = 200;
const button_back = new PIXI.Graphics();
button_back.lineStyle(2, 0x000000, 1)
button_back.beginFill(0xFFFFFF)
button_back.drawRect(0, 0, 84, 84)
button_back.endFill()
button.addChild(button_back)
let modulator = PIXI.Sprite.from('next.png');
modulator.x = 10
modulator.y = 10
// modulator.scale.set(0.5, 0.5);
button.addChild(modulator);
button.buttonMode = true
button.interactive = true;
// button.cacheAsBitmap = true;
app.stage.addChild(button);
const on_button_clicked = async (e) => {
  const response = await axios.post("http://localhost:8080/step");
  move_robot(response.data.loc);
  draw_current_state(response);
  label2.text = response.data.action_prob.join(" , ")
}
button.on('pointerdown', on_button_clicked)

// or container.addChild(container); which is the same
let elapsed = 0.0
let last_mouse_event

const process = (delta) => {
  
  elapsed += delta / 50;
  if (elapsed > 1.0) {
    elapsed -= 1.0;
  }
  
  // aim_update_time += delta;
  // if (aim_update_time > aim_update_delay)
  //   on_mouse_move(last_mouse_event);
}

// app.ticker.add(process);
// mouse interactions
// app.stage.hitArea = app.screen;
// app.stage.interactive = true;
// app.stage.on('mousemove', on_mouse_move)