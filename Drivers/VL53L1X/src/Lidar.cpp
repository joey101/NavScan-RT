#include "Lidar.hpp"
#include <utility> // For std::move

// 1. Default Constructor
Lidar::Lidar()
    : name("Unknown"), health(new int(100)) {
}

// 2. Parameterized Constructor
Lidar::Lidar(std::string n, int h)
    : name(n), health(new int(h)) {
}

// 3. Copy Constructor (Deep Copy)
Lidar::Lidar(const Lidar& other)
    : name(other.name), health(new int(*other.health)) {
}

// 4. Move Constructor
Lidar::Lidar(Lidar&& other) noexcept
    : name(std::move(other.name)), health(other.health) {
    other.health = nullptr; // Steal resource, leave original in safe state
}

// Destructor
Lidar::~Lidar() {
    delete health;
}

// Print Status Function
// void Lidar::print_status() const {
//     if (health) {
//         std::cout << "Name: " << name << ", Health: " << *health << "\n";
//     } else {
//         std::cout << "Name: " << name << " (Moved Out / No Health Data)\n";
//     }
// }

