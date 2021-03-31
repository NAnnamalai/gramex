/* globals uifactory, fields */

uifactory.register({
  name: 'g-email',
  template: /* HTML */`
  <label data-type="email" for="<%= name %>"><%= label %></label>
  <input type="email" class="form-control" name="<%= name %>" id="<%= name %>" aria-describedby="email-<%= name %>"
    placeholder="<%= placeholder %>" pattern="<%= pattern || '.*' %>" value="<%= value %>">
  <% if (typeof help != 'undefined') { %>
    <small id="email-help" class="form-text text-muted"><%= help %></small>
  <% } %>
  `,
  options: fields['g-email']
})
