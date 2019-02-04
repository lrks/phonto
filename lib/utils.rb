require 'rmagick'

module Phonto
  class Utils
    def self.rgb2hsvl(px)
      hsvl = [0, 0, 0, 0]
      max = [px.red, px.green, px.blue].max
      min = [px.red, px.green, px.blue].min

      # H
      if max == min
        hsvl[0] = 0
      elsif min == px.blue
        hsvl[0] = (60 * (px.green - px.red) / (max - min)) + 60
      elsif min == px.red
        hsvl[0] = (60 * (px.blue - px.green) / (max - min)) + 180
      elsif min == px.green
        hsvl[0] = (60 * (px.red - px.blue) / (max - min)) + 300
      end

      # S
      if max == 0
        hsvl[1] = 65535
      else
        hsvl[1] = (max - min) / max
      end

      # V
      hsvl[2] = max

      # L
      hsvl[3] = (max + min) / 2

      return hsvl
    end


    def self.lbp(file)
      image = Magick::ImageList.new(file).first
      image = image.resize_to_fit(300, 300) if [image.columns, image.rows].max > 300

      hist = Array.new(256*4, 0)
      for y in 0...image.rows
        for x in 0...image.columns
          vals = [0, 0, 0, 0]
          this = rgb2hsvl(image.pixel_color(x, y))
          [[0, -1], [-1, -1], [0, -1], [1, -1], [0, 1], [1, 1], [0, 1], [1, -1]].each_with_index do | p, i |
            t = rgb2hsvl(image.pixel_color(x+p[0], y+p[1]))
            for j in 0...4
              vals[j] += (t[j] < this[j]) ? 0 : (2 ** (7 - i))
            end
          end

          hist[vals[0]] += 1
          hist[vals[1] + 256] += 1
          hist[vals[2] + 256*2] += 1
          hist[vals[3] + 256*3] += 1
        end
      end

      div = Math.sqrt(hist.collect{|v| v*v}.sum.to_f)
      return hist.map{|v| v/div}
    end
  end
end
