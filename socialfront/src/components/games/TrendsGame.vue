<template>
  <div class="eg-theme-gourmet ">
    <div class="eg-slideshow">
        <slide :duration="0" enter="bounceInRight" leave="fadeOut">
            <h1>Hi there !</h1>
            <h4>This is your first slideshow !</h4>
        </slide>
        <slide :duration="0" enter="bounceInRight" leave="fadeOut">
            <h3>Hey modify me !</h3>
            <p>Come on modify me ! If you are running the development server, you will see the changes take effect immediately</p>
        </slide>
        <slide :duration="0" enter="bounceInRight" leave="fadeOut">
            <h3>Want cool effects?</h3>
            <p>Code your own, or try stealing for the other slideshows !</p>
        </slide>
    </div>
  </div>
</template>

<script>
import eagle from 'eagle.js'

export default {
  mixins: [ eagle.slideshow ],
  infos: {
    // These infos appear on the home page, below the slideshow's thumbnail
    title: 'Your First Slideshow',
    description: 'A boilerplate to get you started',
    path: 'games'
  }
}
</script>

<style>

</style>
