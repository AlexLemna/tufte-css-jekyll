require 'rubygems'
require 'rake'
require 'rdoc'
require 'date'
require 'yaml'
require 'tmpdir'
require 'jekyll'

desc "Generate blog files"
task :generate do
  Jekyll::Site.new(Jekyll.configuration({
    "source"      => ".",
    "destination" => "docs"
  })).process
end


desc "Generate and publish blog to gh-pages"
task :publish => [:generate] do
  Dir.mktmpdir do |tmp|
    commitmessage = "Commit changes in src"
    system "git commit -am #{commitmessage.shellescape}"
    system "git push origin src --force"
    system "mv _site/* #{tmp}"
    system "git checkout -B gh-pages"
    system "rm -rf *"
    system "mv #{tmp}/* ."
    message = "Site updated at #{Time.now.utc}"
    system "git add ."
    system "git commit -am #{message.shellescape}"
    system "git push origin gh-pages --force"
    system "git checkout src"
    system "echo Done."
  end
end

desc "Generate and publish blog to gh-pages"
task :publishmaster => [:generate] do
  Dir.mktmpdir do |tmp|
    commitmessage = "Commit changes in src"
    system "git commit -am #{commitmessage.shellescape}"
    system "git push origin src --force"
    system "mv _site/* #{tmp}"
    system "git checkout -B master"
    system "rm -rf *"
    system "mv #{tmp}/* ."
    message = "Site updated at #{Time.now.utc}"
    system "git add ."
    system "git commit -am #{message.shellescape}"
    system "git push origin master --force"
    system "git checkout src"
    system "echo Done."
  end
end


task :default => :publish