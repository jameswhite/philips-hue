#!/usr/bin/env ruby
require 'httparty'
require 'json'
require 'pp'

lights = {
           :closent    => [ 1 ],
           :bedroom    => [ 2 ],
           :livingroom => [ 3 ],
           :windows    => [ 4, 5 ],
           :entry      => [ 6, 7 ],
           :bath       => [ 11, 8 , 10 ],
           :laundry    => [ 9 ],
         }

response = HTTParty.get("http://philips-hue/api/#{ENV['HUE_USER']}/lights")
lights = JSON.parse(response.body)
pp lights

# response = HTTParty.get("http://philips-hue/api/#{ENV['HUE_USER']}/lights/3")
# data = JSON.parse(response.body)
# # pp data

# response = HTTParty.put("http://philips-hue/api/#{ENV['HUE_USER']}/lights/3/state",:body =>'{"on":false}')
# data = JSON.parse(response.body)
# # pp data

# Saturation: 255 is the most saturated (colored) and 0 is the least saturated (white).
# Brightness: minimum => 0, maximum => 255. Note a brightness of 0 is not off.
# Hue:        This is a wrapping value between 0 and 65535.
#             Both 0 and 65535 are red, 25500 is green and 46920 is blue.

# [0, 25500, 46920].each do |color|
#   lights.keys.each do |light|
#     response = HTTParty.put("http://philips-hue/api/#{ENV['HUE_USER']}/lights/#{light}/state",:body =>"{\"on\":true, \"sat\":255, \"bri\":255,\"hue\":#{color}}")
#     data = JSON.parse(response.body)
#   end
#   sleep 3
# end
# lights.keys.each do |light|
#   response = HTTParty.put("http://philips-hue/api/#{ENV['HUE_USER']}/lights/#{light}/state",:body =>"{\"on\":true, \"sat\":0, \"bri\":255,\"hue\":25500}")
#   data = JSON.parse(response.body)
# end
# lights.keys.each do |light|
#   response = HTTParty.put("http://philips-hue/api/#{ENV['HUE_USER']}/lights/#{light}/state",:body =>'{"on":false}')
#   data = JSON.parse(response.body)
# end

# response = HTTParty.get("http://philips-hue/api/#{ENV['HUE_USER']}/groups/0")
# data = JSON.parse(response.body)
# pp data

# response = HTTParty.put("http://philips-hue/api/#{ENV['HUE_USER']}/groups/1",:body =>"{\"name\":\"Entry\",\"lights\":[\"6\",\"7\"]}")
# data = JSON.parse(response.body)
# pp data
# [{"error"=> {"type"=>3, "address"=>"/groups/1", "description"=>"resource, /groups/1, not available"}}]

# [0, 25500, 46920].each do |color|
#   response = HTTParty.put("http://philips-hue/api/#{ENV['HUE_USER']}/groups/0/action",:body =>"{\"on\":true, \"sat\":255, \"bri\":255,\"hue\":#{color}}")
#   data = JSON.parse(response.body)
#   pp data
#   sleep 2
# end

red   = 0
green = 25500
blue  = 46920
(1..2).each do |x|
  response = HTTParty.put("http://philips-hue/api/#{ENV['HUE_USER']}/groups/0/action",:body =>"{\"on\":true, \"sat\":255, \"bri\":255,\"hue\":#{red}}")
  sleep 0.6
  response = HTTParty.put("http://philips-hue/api/#{ENV['HUE_USER']}/groups/0/action",:body =>"{\"on\":true, \"sat\":255, \"bri\":128,\"hue\":#{red}}")
  sleep 0.6
end
response = HTTParty.put("http://philips-hue/api/#{ENV['HUE_USER']}/groups/0/action",:body =>"{\"on\":true, \"sat\":0, \"bri\":128,\"hue\":#{green}}")
sleep 3
response = HTTParty.put("http://philips-hue/api/#{ENV['HUE_USER']}/groups/0/action",:body =>'{"on":false}')

# response = HTTParty.get("http://philips-hue/api/#{ENV['HUE_USER']}/schedules")

# response = HTTParty.get("http://philips-hue/api/#{ENV['HUE_USER']}/schedules")
# data = JSON.parse(response.body)
# pp data

# response = HTTParty.get("http://www.meethue.com/api/nupnp")
# data = JSON.parse(response.body)
# pp data
