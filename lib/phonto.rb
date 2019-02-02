require "phonto/version"

module Phonto
  class Error < StandardError; end

  class CLI
    def initialize(model_dir)
      @model_dir = model_dir
    end

    def train(photo_dir, illust_dir)
      p photo_dir, illust_dir, @model_dir
      return 0
    end

    def classify(image_file)
      p image_file, @model_dir
      return 0
    end
  end
end
