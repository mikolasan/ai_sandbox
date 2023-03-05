import random from './isaac.js';
import { calc_angle, calc_distance, x_cell, y_cell, grid } from './world.js';
import { findPath } from './astar.js';

let range_x_min = 0;
let range_x_max = 3 * x_cell;

let range_y_min = 0;
let range_y_max = 3 * y_cell;

let n = 10

let r_x = range_x_max / 2;
let r_y = range_y_max / 2;

let i = 0;

while (i < n) {
  let random_x = random(range_x_min, range_x_max);
  let random_y = random(range_y_min, range_y_max);
  let x2 = Math.floor(random_x / x_cell);
  let y2 = Math.floor(random_y / y_cell);
  console.log(x2, y2)
  if (x2 == 2 && y2 == 2) {
    console.log(`(${random_x}, ${random_y}) - this is where the robot stands`)
    continue;
  }
  let a = calc_angle(r_x, r_y, random_x, random_y);
  let d = calc_distance(r_x, r_y, random_x, random_y);
  console.log(`${a},${d}`)
  
  var start = grid[2][2];
  var goal = grid[x2][y2];
  let path = findPath(start, goal)
  console.log(path.reverse().map((node) => node.coord))
  
  ++i;
}

// for (let x = 0; x < grid.length; ++x) {
//   let line = '';
//   for (let y = 0; y < grid[x].length; ++y) {
//     const node = grid[x][y];
//     line += node.coord + ' '
//   }
//   console.log(line)
// }

// console.log(grid[2][2].neighbours(null).map((node) => node.coord))
