import * as PIXI from 'pixi.js';

// Create the application helper and add its render target to the page
let app = new PIXI.Application({
  width: 800,
  height: 640,
  background: '#daddd8',
  antialias: true
});
let root = document.getElementsByClassName("pixi-canvas");
if (root.length > 0) {
  root[0].appendChild(app.view);
} else {
  console.error(`Where's "pixi-canvas"?`)
}

let graphics = new PIXI.Graphics();

let elapsed = 0.0
let total_elapsed = 0.0
let frame_counter = 0
let frame_counter_start_time
let fps = 0.0

const level_x = 50;
const level_y = 50;
const level_border = 2;
const level_width = 20;
const level_height = 300;


const draw_bar = function(graphics, value) {
  graphics.lineStyle(level_border, 0x000000, 1)
  graphics.beginFill(0xFFFFFF);
  graphics.drawRect(
    level_x,
    level_y,
    level_width,
    level_height);
  graphics.endFill();
  graphics.lineStyle(0)
  graphics.beginFill(0xb7ce63);
  const fill_start_y = level_height * (1 - value / 100)
  graphics.drawRect(
    level_x + level_border / 2,
    level_y + fill_start_y + level_border / 2,
    level_width - level_border,
    level_height - fill_start_y - level_border);
  graphics.endFill();
  return graphics
}

const max_limit = 100 // K
const normal_level = 50 // M
const pump_value_default = 20 // N
const growth_rate = 0.2 // r
const decay_rate = 0.01 // s
let level_value = normal_level;
let pump_value = 0.0
// let pump_time
let release_value = 0.0

graphics = draw_bar(graphics, level_value)
app.stage.addChild(graphics);

const button = new PIXI.Container();
button.x = level_x - 15;
button.y = level_y + level_height + 40;
const button_back = new PIXI.Graphics();
button_back.lineStyle(2, 0x000000, 1)
button_back.beginFill(0xFFFFFF)
button_back.drawRect(0, 0, 50, 50)
button_back.endFill()
button.addChild(button_back)
let modulator = PIXI.Sprite.from('chemistry.png');
modulator.x = 10
modulator.y = 10
// modulator.scale.set(0.5, 0.5);
button.addChild(modulator);
button.buttonMode = true
button.interactive = true;
// button.cacheAsBitmap = true;
app.stage.addChild(button)

const basicText = new PIXI.Text("FPS: " + fps);
basicText.x = 500;
basicText.y = 10;

// const process = (delta) => {
//   total_elapsed += delta / 50
//   if (pump_time !== undefined && level_value < 100) {
//     elapsed = delta;
//     decay = pump_value_default * (total_elapsed - pump_time) * Math.exp(pump_time - total_elapsed)
//     console.log(pump_time, total_elapsed, decay)
//     if (Math.abs(decay) < 1e-2) {
//       pump_time = undefined
//     }

//     level_value = 50 + decay
//     if (level_value > 100) {
//       level_value = 100
//     }
//     graphics = draw_bar(graphics, level_value)
//   }
// }

const process = (delta) => {
  ++frame_counter;
  if (!frame_counter_start_time) {
    frame_counter_start_time = performance.now()
  } else {
    const now = performance.now()
    if (now - frame_counter_start_time > 1000) {
      frame_counter_start_time = now
      fps = frame_counter
      basicText.text = "FPS: " + fps
      frame_counter = 0
    }
  }

  // total_elapsed += delta / 50
  if (pump_value > 0.0 || release_value > 0.0) {
    // elapsed = delta;
    const prev_level = level_value

    let growth = 0.0
    let decay = 0.0

    growth = growth_rate * pump_value
    pump_value -= growth
    release_value += growth

    decay = decay_rate * release_value
    release_value -= decay

    level_value += growth - decay;

    if (Math.abs(growth) < 1e-2) {
      growth = 0.0
      pump_value = 0.0
    }

    if (Math.abs(decay) < 1e-2) {
      decay = 0.0
      release_value = 0.0
    }
    
    graphics = draw_bar(graphics, level_value)
    // console.log(pump_value, release_value)

  }
}

// const process = (delta) => {
//   total_elapsed += delta
//   if (pump_value > 0 && level_value < 100) {
//     elapsed = delta;
//     // decay = pump_value_default * (total_elapsed - pump_time) * Math.exp(pump_time - total_elapsed)
//     // console.log(pump_time, total_elapsed, decay)
//     level_value += elapsed
//     pump_value -= elapsed
//     if (level_value > 100) {
//       level_value = 100
//     }
//     graphics = draw_bar(graphics, level_value)
//     if (pump_value < 0) {
//       pump_value = 0
//     }
//   }
// }


const on_button_clicked = function(e) {
  // pump_time = total_elapsed
  pump_value += pump_value_default
  if (pump_value + level_value > 100) {
    pump_value = 100 - level_value
  }
  // release_value = 0.0
}



app.stage.addChild(basicText);


button.on('pointerdown', on_button_clicked)
app.ticker.add(process);

// mouse interactions
// app.stage.hitArea = app.screen;
// app.stage.interactive = true;
// app.stage.on('mousemove', on_mouse_move)