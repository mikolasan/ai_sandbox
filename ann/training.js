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

// while (i < n) {
//   let random_x = random(range_x_min, range_x_max);
//   let random_y = random(range_y_min, range_y_max);
//   if (random_x > 1 * x_cell && random_x < 2 * x_cell &&
//       random_y > 1 * y_cell && random_y < 2 * y_cell) {
//     console.log(`(${random_x}, ${random_y}) - this is where the robot stands`)
//     continue;
//   }
//   let a = calc_angle(r_x, r_y, random_x, random_y);
//   let d = calc_distance(r_x, r_y, random_x, random_y);
//   console.log(`${a},${d}`)
//   ++i;
// }

// for (let x = 0; x < grid.length; ++x) {
//   let line = '';
//   for (let y = 0; y < grid[x].length; ++y) {
//     const node = grid[x][y];
//     line += node.coord + ' '
//   }
//   console.log(line)
// }

// console.log(grid[2][2].neighbours(null).map((node) => node.coord))
let path = findPath(grid[2][2], grid[0][0])
console.log(path)

// var start = grid[x][y];
// var goal = grid[x2][y2];