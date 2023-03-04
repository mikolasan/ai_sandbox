// by Will Thimbleby

// global vars used to adjust the algorithm
// not necessary for real use

var allowDiagonals = false
var diagonalCost
var dotTiebreaker = false
var badSorting = false

// insert sort for better priority queue performance
Array.prototype.insertSorted = function(v, sortFn) {
    if(this.length < 1 || sortFn(v, this[this.length-1]) >= 0) {
        this.push(v);
        return this;
    }
	for(var i=this.length-2; i>=0; --i) {
        if(sortFn(v, this[i]) >= 0) {
            this.splice(i+1, 0, v);
            return this;
        }
    }
	this.splice(0, 0, v);
	return this;
}

// for comparison this insert sort uses > not >= thus inserting new nodes nearer the back
// this provides much worse searching
Array.prototype.insertSorted2 = function(v, sortFn) {
    if(this.length < 1 || sortFn(v, this[this.length-1]) > 0) {
        this.push(v);
        return this;
    }
	for(var i=this.length-2; i>=0; --i) {
        if(sortFn(v, this[i]) > 0) {
            this.splice(i+1, 0, v);
            return this;
        }
    }
	this.splice(0, 0, v);
	return this;
}

class Node {
  constructor(x, y, wall, map) {
    this.x = x;
    this.y = y;
    this.wall = wall;
    this.map = map;
    this.coord = x + ":" + y;
    this.neighbours = function (goal) {
      var n = [];

      var dir = [[0, 1], [0, -1], [1, 0], [-1, 0], [1, 1], [-1, 1], [1, -1], [-1, -1]];
      for (var i = 0; i < (allowDiagonals ? 8 : 4); ++i) {
        if (this.x + dir[i][0] < 0 || this.x + dir[i][0] > this.map.length)
          continue;
        if (this.y + dir[i][1] < 0 || this.y + dir[i][1] > this.map[x].length)
          continue;

        var p = this.map[this.x + dir[i][0]][this.y + dir[i][1]];
        // console.log(p)
        if (p.wall && p != goal)
          continue;

        n.push(p);
      }
      return n;
    };
  }
}

function h(a, b) {
	var cross = 0;
	if(dotTiebreaker) {
		var dx1 = a.x - b.x
		var dy1 = a.y - b.y
		var dx2 = start.x - b.x
		var dy2 = start.y - b.y
		var cross = Math.abs(dx1*dy2 - dx2*dy1)
	}
	
	if(allowDiagonals) {
		var straight = Math.abs(Math.abs(a.x-b.x) - Math.abs(a.y-b.y));
		var diagonal = Math.max(Math.abs(a.x-b.x), Math.abs(a.y-b.y)) - straight;
		return straight + diagonalCost*diagonal + cross*0.001;
		//return Math.max(Math.abs(a.x-b.x), Math.abs(a.y-b.y)); simple version
	}
	return Math.abs(a.x-b.x)+Math.abs(a.y-b.y) + cross*0.001;
}

function findPath(start, goal) {
	var closed = {};
	var open = [start];
	
	var g_score = {}; // distance from start along optimal path
	var f_score = {}; // estimated distance from start to goal through node
	
	g_score[start.coord] = 0;
	f_score[start.coord] = h(start, goal);
	
	var cameFrom = {};
	
	var sortFn = function(b, a) {return f_score[a.coord] - f_score[b.coord];};
	
	while(open.length > 0) {
		var node = open.pop(); // node with lowest f score
		if(node == goal) {
			var path = [goal];
			while(cameFrom[path[path.length-1].coord]) {
				path.push(cameFrom[path[path.length-1].coord])
			}
			return path;
		}
		closed[node.coord] = true;
		
		var neighbours = node.neighbours(goal);
		for(var i=0,c=neighbours.length;i<c;++i) {
			var next = neighbours[i];
			if(closed[next.coord]) continue;
			
			var diagonal = next.x != node.x && next.y != node.y;
			
			var temp_g_score = g_score[node.coord] + (diagonal?diagonalCost:1);
			var isBetter = false;
			
			var idx = open.indexOf(next);
			if(idx < 0) {
			  isBetter = true;
				// nodesSearched++;
			}
			else if(temp_g_score < g_score[next.coord]) {
			    open.splice(idx, 1); // remove old node
				isBetter = true;
			}
			
			if(isBetter) {
				cameFrom[next.coord] = node;
				g_score[next.coord] = temp_g_score;
				f_score[next.coord] = g_score[next.coord] + h(next, goal);
				
				// add the new node or reinsert the old node
				if(badSorting) open.insertSorted2(next, sortFn);
                else open.insertSorted(next, sortFn);
										    
				// drawing
				// var s = Math.floor(g_score[next.coord]*4);
				// ctx.fillStyle = 'rgb('+(255-s)+',255,'+s+')';
				// ctx.fillRect(next.x*10, next.y*10, 10, 10);
			}
		}
	}
	// fail
	return [];
}

export { findPath, Node }