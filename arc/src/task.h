#include <chrono>
#include <iostream>
#include <list>
#include <memory>
#include <thread>

class Task {
public:
  virtual ~Task() = default;
  virtual void run() = 0;
};

class SimpleTask : public Task {
  void run() {
    using std::chrono::operator""ms;
    std::this_thread::sleep_for(100ms);
  }
};