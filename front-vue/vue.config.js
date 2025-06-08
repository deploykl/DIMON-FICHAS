const { defineConfig } = require('@vue/cli-service')
const webpack = require('webpack')
module.exports = defineConfig({
  transpileDependencies: true,

  devServer: {
    port: 8080, // Configura el puerto a 80
    host: '0.0.0.0', // Permite conexiones desde cualquier IP
    https: false, // Cambia a true si necesitas HTTPS
  },
  configureWebpack: {
    plugins:[
      new webpack.DefinePlugin({
        '__VUE_PROD_HYDRATION_MISMATCH_DETAILS__': JSON.stringify(false),
      })
    ]
  }
})
