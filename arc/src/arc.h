#include <map>
#include <string>
#include <vector>

#include "math.h"

std::vector<Example> read_training_data(std::string task_id);

// some round symbols take extra space,
// so I'm replacing them with other symbols of the same color
static std::map<int, std::string> color_map = {
  {0, "⚫️"}, // black
  {1, "🔵"}, // blue
  {2, "🔴"}, // red
  {3, "🍏"}, // green
  {4, "🍋"}, // yellow
  {5, "⚪️"}, // grey
  {6, "💗"}, // fuschia (pink)
  {7, "🟠"}, // orange
  {8, "🔮"}, // teal (light blue)
  {9, "🟤"}, // brown
};

using ThreeColorSaturation = std::tuple<int,int,int>;

constexpr int quantization_level = 5;
constexpr int color_min = 0;
constexpr int color_max = 255;

constexpr int quantize(int value, int a, int b) {
  const int interval_size = (b - a) / quantization_level;
  return value / interval_size;
} 

constexpr ThreeColorSaturation make_quantized_tuple(int r, int g, int b) {
  return std::make_tuple(
    quantize(r, color_min, color_max),
    quantize(g, color_min, color_max),
    quantize(b, color_min, color_max));
}

static std::map<int, ThreeColorSaturation> value_to_saturations_map = {
  {0, make_quantized_tuple(0,0,0)}, // black
  {1, make_quantized_tuple(0,116,217)}, // blue
  {2, make_quantized_tuple(255,65,54)}, // red
  {3, make_quantized_tuple(46,204,64)}, // green
  {4, make_quantized_tuple(255,220,0)}, // yellow
  {5, make_quantized_tuple(170,170,170)}, // grey
  {6, make_quantized_tuple(240,18,190)}, // fuschia (pink)
  {7, make_quantized_tuple(255,133,27)}, // orange
  {8, make_quantized_tuple(127,219,255)}, // teal (light blue)
  {9, make_quantized_tuple(135,12,37)}, // brown
};