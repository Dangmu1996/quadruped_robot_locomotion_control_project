#include <memory>
#include <string>

#include "geometry_msgs/msg/transform_stamped.hpp"
#include "nav_msgs/msg/odometry.hpp"
#include "rclcpp/rclcpp.hpp"
#include "tf2_ros/transform_broadcaster.h"

class OdomToTfBroadcaster : public rclcpp::Node
{
public:
  OdomToTfBroadcaster()
  : Node("odom_to_tf_broadcaster")
  {
    odom_topic_ = this->declare_parameter<std::string>("odom_topic", "/odom");
    odom_frame_id_ = this->declare_parameter<std::string>("odom_frame_id", "odom");
    base_frame_id_ = this->declare_parameter<std::string>("base_frame_id", "base");

    tf_broadcaster_ = std::make_unique<tf2_ros::TransformBroadcaster>(*this);

    odom_sub_ = this->create_subscription<nav_msgs::msg::Odometry>(
      odom_topic_, 10,
      std::bind(&OdomToTfBroadcaster::odom_callback, this, std::placeholders::_1));

    RCLCPP_INFO(this->get_logger(), "Subscribed to odom topic: %s", odom_topic_.c_str());
    RCLCPP_INFO(this->get_logger(), "Broadcasting TF: %s -> %s", odom_frame_id_.c_str(), base_frame_id_.c_str());
  }

private:
  void odom_callback(const nav_msgs::msg::Odometry::SharedPtr msg)
  {
    geometry_msgs::msg::TransformStamped t;

    t.header.stamp = msg->header.stamp;
    t.header.frame_id = odom_frame_id_;
    t.child_frame_id = base_frame_id_;

    t.transform.translation.x = msg->pose.pose.position.x;
    t.transform.translation.y = msg->pose.pose.position.y;
    t.transform.translation.z = msg->pose.pose.position.z;

    t.transform.rotation = msg->pose.pose.orientation;

    tf_broadcaster_->sendTransform(t);
  }

  std::string odom_topic_;
  std::string odom_frame_id_;
  std::string base_frame_id_;

  rclcpp::Subscription<nav_msgs::msg::Odometry>::SharedPtr odom_sub_;
  std::unique_ptr<tf2_ros::TransformBroadcaster> tf_broadcaster_;
};

int main(int argc, char * argv[])
{
  rclcpp::init(argc, argv);
  rclcpp::spin(std::make_shared<OdomToTfBroadcaster>());
  rclcpp::shutdown();
  return 0;
}
