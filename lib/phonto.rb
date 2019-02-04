require 'phonto/version'
require_relative './utils.rb'
require 'fileutils'
require 'svmkit'

module Phonto
  class Error < StandardError; end

  class CLI
    def initialize(model_dir)
      FileUtils.mkdir_p(model_dir)
      @model_dir = model_dir
    end

    def prepare(photo_dir, illust_dir)
      def calc(dir, label, dst_lbps, dst_labels)
        i = 0
        Dir.glob("#{dir}/*.*").each_with_index do | file, idx |
          next unless file.match?(/\.(?:jpg|jpeg|png|gif|bmp)/i)
          puts "load #{idx}, #{File.basename(file)}, label=#{label}"
          dst_lbps << Utils.lbp(file)
          dst_labels << label
          i += 1
          break if i > 100
        end
      end

      lbps = []
      labels = []
      calc(photo_dir, 0, lbps, labels)
      calc(illust_dir, 1, lbps, labels)
      File.binwrite("#{@model_dir}/lbps.dat", Marshal.dump(Numo::DFloat.cast(lbps)))
      File.binwrite("#{@model_dir}/labels.dat", Marshal.dump(Numo::Int32.cast(labels)))
    end

    def tune(gamma, random_seed)
      lbps = Marshal.load(File.binread("#{@model_dir}/lbps.dat"))
      labels = Marshal.load(File.binread("#{@model_dir}/labels.dat"))

      # svmkit Example 3. Pipeline
      rbf = SVMKit::KernelApproximation::RBF.new(gamma: gamma, n_components: 1024, random_seed: random_seed)
      svc = SVMKit::LinearModel::SVC.new(reg_param: gamma, max_iter: 1000, random_seed: random_seed)
      pipeline = SVMKit::Pipeline::Pipeline.new(steps: { trns: rbf, clsf: svc })

      kf = SVMKit::ModelSelection::StratifiedKFold.new(n_splits: 5, shuffle: true, random_seed: random_seed)
      cv = SVMKit::ModelSelection::CrossValidation.new(estimator: pipeline, splitter: kf)
      report = cv.perform(lbps, labels)
      mean_accuracy = report[:test_score].inject(:+) / kf.n_splits
      puts("5-CV mean accuracy: %.1f %%" % (mean_accuracy * 100.0))
    end

    def classify(image_file)
      p image_file, @model_dir
    end
  end
end
