# CS50W-Projects
All projects of CS50's Web Programming with Python and JavaScript

### Table of Content
- [Network](#network)
- [Commerce](#commerce)
- [Mail](#mail)
- [Wiki](#wiki)
- [Search](#search)
<br/>

Every project has a screenshots directory for a sneak peek of the project
IDEs used: **_PyCharm_** for Django, **_WebStorm_** (For Frontend Project Only)

## Network
A Twitter-like social network website for making posts, following users, adding comments, etc.

<img src="https://github.com/ModyElSayed/CS50W-Projects/blob/master/project4/screenshots/home_1.png"><br/>

### Specification
- **New Post**: Users who are signed in are able to write a new text-based post by filling in text into a text area and then clicking a button to submit the post.
- **All Posts**: The “All Posts” link in the navigation bar takes the user to a page where they can see all posts from all users, with the most recent posts first.
- **Profile Page**: Clicking on a username loads that user’s profile page. This page:
  - Display the number of followers the user has, as well as the number of people that the user follows.
  - Display all the posts for that user, in reverse chronological order.
  - For any other user who is signed in, this page also display a “Follow” or “Unfollow” button that will let the current user toggle whether or not they are following this user’s posts. Note that this only applies to any “other” user: a user is not able to follow themselves.
- **Following**: The “Following” link in the navigation bar takes the user to a page where they see all posts made by users that the current user follows.
- **Pagination**: On any page that displays posts, posts are only displayed 10 on a page. If there are more than ten posts, a “Next” button appears to take the user to the next page of posts. If not on the first page, a “Previous” button appears to take the user to the previous page of posts as well.
- **Edit Post**: Users are able to click an “Edit” button on any of their own posts to edit that post. It does not allow editing more than 1 post at the same time.
  - When a user clicks “Edit” for one of their own posts, the content of their post is replaced with a `textarea` where the user can edit the content of their post.
  - For security, the application is designed such that it is not possible for a user, via any route, to edit another user’s posts.
- **“Like”** and **“Unlike”**: Users are able to click the like button on any post to toggle whether or not they “like” that post.
- **Comments**: Users are able to add comments to any post.

###### Frontend: HTML, CSS, Javascript, and Bootstrap<br/>Backend: Django<br/>Directory: project4

## Mail
Front-end for an email client that makes API calls to send and receive emails.

<img src="https://github.com/ModyElSayed/CS50W-Projects/blob/master/mail/screenshots/inbox.png"><br/>

### Specification
Using JavaScript, HTML, and CSS, it's an implementation of a single-page-app email client inside of `inbox.js`
- **Send Mail**: When a user submits the email composition form.
  - A `POST` request to `/emails`, passing in values for `recipients`, `subject`, and `body`.
  - Once the email has been sent, load the user’s sent mailbox.
- **Mailbox**: When a user visits their Inbox, Sent mailbox, or Archive, it loads the appropriate mailbox.
  - When a mailbox is visited, the application first query the API for the latest emails in that mailbox.
  - If the email is unread, it appears with a white background. If the email has been read, it appears with a gray background.
- **View Email**: When a user clicks on an email, the user is taken to a view where they see the content of that email.
  - The application shows the email’s sender, recipients, subject, timestamp, and body.
  - Once the email has been clicked on, the application marks the email as read.
- **Archive and Unarchived**: Users are able to archive and unarchived emails that they have received.
  - When viewing an Inbox email, the user is presented with a button that lets them archive the email. When viewing an Archive email, the user is presented with a button that lets them unarchived the email. 
  - Once an email has been archived or unarchived, load the user’s inbox.
- **Reply**: Users are able to reply to an email.
  - When viewing an email, the user is presented with a “Reply” button that lets them reply to the email.
  - When the user clicks the “Reply” button, they are taken to the email composition form.
  - The composition form is pre-filled with the `recipient` field set to whoever sent the original email.
  - The `subject` line is pre-filled. If the original email had a subject line of `foo`, the new subject line is `Re: foo`. (If the subject line already begins with `Re: `, it's not added again.)
  - The `body` of the email is pre-filled with a line like `"On Jan 1 2020, 12:00 AM foo@example.com wrote:"` followed by the original text of the email.

###### Frontend: HTML, CSS, Javascript, and Bootstrap<br/>Directory: mail

## Commerce
An **eBay-like** e-commerce auction site that will allow users to post auction listings, place bids on listings, comment on those listings, and add listings to a “watchlist.”

<img src="https://github.com/ModyElSayed/CS50W-Projects/blob/master/commerce/screenshots/auction_listings.png"><br/>

### Specification
- **Create Listing**: Users can visit a page to create a new listing. They can specify a title for the listing, a text-based description, and what the starting bid should be. Users also optionally can provide a URL for an image for the listing and/or a category (e.g. Fashion, Toys, Electronics, Home, etc.).
- **Active Listings Page**: Users can view all the currently active auction listings. For each active listing, this page display (at minimum) the title, description, current price, and photo (if one exists for the listing).
- **Listing Page**: Clicking on a listing takes users to a page specific to that listing. On that page, users are able to view all details about the listing, including the current price for the listing.
  - If the user is signed in, the user is able to add the item to their “Watchlist.” If the item is already on the watchlist, the user is able to remove it.
  - If the user is signed in, the user is able to bid on the item. The bid must be at least as large as the starting bid, and must be greater than any other bids that have been placed (if any). If the bid doesn’t meet those criteria, the user is presented with an error.
  - If the user is signed in and is the one who created the listing, the user have the ability to “close” the auction from this page, which makes the highest bidder the winner of the auction and makes the listing no longer active.
  - If a user is signed in on a closed listing page, and the user has won that auction, the page say so. 
  - Users who are signed in are able to add comments to the listing page. The listing page displays all comments that have been made on the listing.
- **Watchlist**: Users who are signed in can visit a **Watchlist** page, which displays all the listings that a user has added to their watchlist. Clicking on any of those listings takes the user to that listing’s page. 
- **Categories**: Users can visit a page that displays a list of all listing categories. Clicking on the name of any category takes the user to a page that displays all the active listings in that category.
- **Models**: The application have 5 models: `User`, `AuctionListings`, `ListingComments`, `ListingBids`, `Watchlist`.
- **Django Admin Interface**: Via the Django admin interface, a site administrator can view, add, edit, and delete any listings, comments, and bids made on the site.

###### Frontend: HTML, CSS, and Bootstrap<br/>Backend: Django<br/>Directory: commerce

## Wiki
A **Wikipedia-like** online encyclopedia. Each encyclopedia entry will be saved as a Markdown file

<img src="https://github.com/ModyElSayed/CS50W-Projects/blob/master/commerce/screenshots/home.png"><br/>

### Specification
- **Entry Page**: Visiting `/wiki/TITLE`, where `TITLE` is the title of an encyclopedia entry, render a page that displays the contents of that encyclopedia entry. 
- **Home Page**: Listing the names of all pages in the encyclopedia, user can click on any entry name to be taken directly to that entry page.
- **Search**: The user can type a query into the search box in the sidebar to search for an encyclopedia entry.
    - If the query matches the name of an encyclopedia entry, the user should be redirected to that entry’s page.
    - If the query does not match the name of an encyclopedia entry, the user instead is taken to a search results page that displays a list of all encyclopedia entries that have the query as a substring. For example, if the search query were `ytho`, then `Python` appear in the search results.
    - Clicking on any of the entry names on the search results page takes the user to that entry’s page.
- **Create New Page**:  Clicking “Create New Page” in the sidebar takes the user to a page where they can create a new encyclopedia entry.
  - The user can enter a title for the page, and to enter the Markdown content for the page.
  - When the page is saved, if an encyclopedia entry already exists with the provided title, the user is presented with an error message.
- **Edit Page**: On each entry page, the user can click a link to be taken to a page where the user can edit that entry’s Markdown content.
- **Random Page**: Clicking “Random Page” in the sidebar should take user to a random encyclopedia entry.

###### Frontend: HTML, CSS, and Bootstrap<br/>Backend: Django<br/>Directory: wiki

## Search
Front-end for _**Google Search**_, _**Google Image Search**_, and **_Google Advanced Search_** as well as the ability to do search for every type of search.

### Specification
 
- On the **Google Search** page, the user can type a query, click “Google Search”, and be taken to the Google search results for that page.
- On the **Google Image Search** page, the user can type a query, click a search button, and be taken to the Google Image search results for that page.
* On the **Google Advanced Search** page, the user can provide input for the following four fields (taken from Google’s own advanced search options)
  - Find pages with… “all these words:”
  - Find pages with… “this exact word or phrase:”
  - Find pages with… “any of these words:”
  - Find pages with… “none of these words:”

###### Front-end: HTML, and CSS<br/>Directory: search
