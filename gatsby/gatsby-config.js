module.exports = {
  pathPrefix: `/tomoteam-catalog`,
  siteMetadata: {
    title: 'tomoteam catalog',
    subtitle: 'sharing favourite solutions for cryoet + teamtomo',
    catalog_url: 'https://github.com/kephale/tomoteam-catalog.git',
    menuLinks:[
      {
         name:'Catalog',
         link:'/catalog'
      },
      {
         name:'About',
         link:'/about'
      },
    ]
  },
  plugins: [{ resolve: `gatsby-theme-album`, options: {} }],
}
