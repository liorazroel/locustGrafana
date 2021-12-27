curl -d "user_count=10&spawn_rate=10.0&host=https%3A%2F%2Freqres.in" -H "Content-Type: application/x-www-form-urlencoded" http://192.168.1.102:4200/swarm
curl -X GET http://192.168.1.102:4200/stop