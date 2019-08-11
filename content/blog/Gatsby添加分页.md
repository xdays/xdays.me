---
title: Gatsby添加分页
date: 2019-08-11
author: admin
category: devops
tags: blog,gatsby
slug: Gatsby添加分页
---

由于我现在的博客文章比较多了，而我基于Gatsby的博客又只有文章页和索引页两个页面，这样索引页看起来就特别长，这就有了分页的需求。本文主要学习[这篇文章](https://nickymeuleman.netlify.com/blog/gatsby-pagination)得来，[gatsby-paginated-blog](https://github.com/NickyMeuleman/gatsby-paginated-blog)也是基于[gatsby-starter-blog](https://github.com/gatsbyjs/gatsby-starter-blog)的。

# 关于Gatsby

这次添加分页读了一下[官方的教程](https://www.gatsbyjs.org/tutorial/), 对Gatsby多了一些理解：



Gatsby的数据是存在graphql里的，而数据是插件处理生成的，比如最重要的两个插件：

1. `gatsby-source-filesystem`在graphql里新增了`allFile`和`file`两个object
2. `gatsby-transformer-remark`新增了`allMarkdownRemark`和`markdownRemark`两个object



Gatsby不区分page和post，内部都称为page，所以在`gatsby-node.js`里只有`createPage`这个接口。那如果要对博客索引分页就要模板化`src/pages/index.js`这个页面。



# 添加分页



所有的改动都在[这次commit](https://github.com/xdays/xdays.me/commit/75368a606fb847b4bfcf35c98f5e19de7041631b)里了 



## 模板化索引页

首先将博客索引页重命名并挪到templates目录下：

```bash
mv src/pages/index.js src/templates/blog-list.js
```

修改graphql查询，添加skip和limit两个参数，来获取特定页面里的内容。

```javascript
export const pageQuery = graphql`
  query blogPageQuery($skip: Int!, $limit: Int!) {
    site {
      siteMetadata {
        title
      }
    }
    allMarkdownRemark(
      sort: { fields: [frontmatter___date], order: DESC }
      limit: $limit
      skip: $skip
    ) {
      edges {
        node {
          excerpt
          fields {
            slug
          }
          frontmatter {
            date(formatString: "MMMM DD, YYYY")
            title
          }
        }
      }
    }
  }
`
```

渲染索引页的时候还需要知道总共有多少页以及当年在第几页，这些都是作为pros传递给索引页的组件的。

```javascript
    const { currentPage, numPages } = this.props.pageContext
    const isFirst = currentPage === 1
    const isLast = currentPage === numPages
    const prevPage = currentPage - 1 === 1 ? '/' : (currentPage - 1).toString()
    const nextPage = (currentPage + 1).toString()
```

然后上一步初始化的几个变脸主要供分页导航里的逻辑使用的。

```jsx
        <ul
          style={{
            display: 'flex',
            flexWrap: 'wrap',
            justifyContent: 'space-between',
            alignItems: 'center',
            listStyle: 'none',
            padding: 0,
          }}
        >
          {!isFirst && (
            <Link to={prevPage} rel="prev">
              ← Previous Page
            </Link>
          )}
          {Array.from({ length: numPages }, (_, i) => (
            <li
              key={`pagination-number${i + 1}`}
              style={{
                margin: 0,
              }}
            >
              <Link
                to={`/${i === 0 ? '' : i + 1}`}
                style={{
                  padding: rhythm(1 / 4),
                  textDecoration: 'none',
                  color: i + 1 === currentPage ? '#ffffff' : '',
                  background: i + 1 === currentPage ? '#007acc' : '',
                }}
              >
                {i + 1}
              </Link>
            </li>
          ))}
          {!isLast && (
            <Link to={nextPage} rel="next">
              Next Page →
            </Link>
          )}
        </ul>
```

至此索引页模板化完成。



## 创建博客索引页

刚才说了所有的页面都是通过`createPage`这个接口创建，所以我们在`gatsby-node.js`里添加创建博客索引页页面的代码，然后通过context给组件传递对应的props就可以了

```javascript
        // Create blog post list pages
        const postsPerPage = 20
        const numPages = Math.ceil(posts.length / postsPerPage)

        Array.from({ length: numPages }).forEach((_, i) => {
          createPage({
            path: i === 0 ? `/` : `/${i + 1}`,
            component: path.resolve('./src/templates/blog-list.js'),
            context: {
              limit: postsPerPage,
              skip: i * postsPerPage,
              numPages,
              currentPage: i + 1,
            },
          })
        })
```

先计算出一共分多少页，然后通过`forEach`创建所有的索引页。