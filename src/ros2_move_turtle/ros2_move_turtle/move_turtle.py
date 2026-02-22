import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist
from turtlesim.msg import Pose

class MoveTurtle(Node):
    def __init__(self):
        super().__init__('move_turtle')
        # Publicador: envía velocidad a la tortuga
        self.publisher = self.create_publisher(Twist, '/turtle1/cmd_vel', 10)
        # Suscriptor: recibe la posición de la tortuga
        self.subscription = self.create_subscription(Pose, '/turtle1/pose', self.pose_callback, 10)
        
        self.get_logger().info('Nodo move_turtle iniciado. Vigilando límites...')

    def pose_callback(self, msg):
        vel_msg = Twist()
        # Lógica de seguridad: si x o y > 7m, se detiene
        if msg.x > 7.0 or msg.y > 7.0:
            vel_msg.linear.x = 0.0
            vel_msg.angular.z = 0.0
            # Solo deja el string con la f-fstring, sin el "True,"
            self.get_logger().warn(f"¡Límite alcanzado! Parando en x:{msg.x:.2f}, y:{msg.y:.2f}")
        else:
            vel_msg.linear.x = 1.0
            vel_msg.angular.z = 0.5
            
        self.publisher.publish(vel_msg)
        vel_msg = Twist()
        
        # Lógica de seguridad: si x o y > 7m, se detiene
        if msg.x > 7.0 or msg.y > 7.0:
            vel_msg.linear.x = 0.0
            vel_msg.angular.z = 0.0
            self.get_logger().warn(f"¡Límite alcanzado! Parando en x:{msg.x:.2f}, y:{msg.y:.2f}")
        else:
            # Si es seguro, que se mueva hacia adelante y gire un poco
            vel_msg.linear.x = 1.0
            vel_msg.angular.z = 0.5
            
        self.publisher.publish(vel_msg)

def main(args=None):
    rclpy.init(args=args)
    node = MoveTurtle()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()