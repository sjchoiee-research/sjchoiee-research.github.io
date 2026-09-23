(function () {
  'use strict';

  function start() {
    var toastTimer;
    var toast = document.getElementById('toast');

    function notify(message) {
      if (!toast) {
        toast = document.createElement('div');
        toast.id = 'toast';
        toast.className = 'toast';
        toast.setAttribute('role', 'status');
        toast.setAttribute('aria-live', 'polite');
        toast.setAttribute('aria-atomic', 'true');
        document.body.appendChild(toast);
      }
      clearTimeout(toastTimer);
      toast.textContent = message;
      toast.hidden = false;
      toast.classList.add('visible');
      toastTimer = setTimeout(function () {
        toast.classList.remove('visible');
        toast.hidden = true;
      }, 4500);
    }

    function download(content, filename, mime) {
      var blob = new Blob([content], { type: mime });
      var url = URL.createObjectURL(blob);
      var link = document.createElement('a');
      link.href = url;
      link.download = filename;
      link.hidden = true;
      document.body.appendChild(link);
      link.click();
      link.remove();
      setTimeout(function () { URL.revokeObjectURL(url); }, 1000);
    }

    function normalize(value) {
      return String(value == null ? '' : value).normalize('NFKC').toLowerCase().trim();
    }

    function text(value) {
      return String(value == null ? '' : value).replace(/\s+/g, ' ').trim();
    }

    var menuToggle = document.querySelector('.menu-toggle');
    var mainNav = document.querySelector('.main-nav');
    if (menuToggle && mainNav) {
      function setMenu(open, restoreFocus) {
        mainNav.classList.toggle('open', open);
        menuToggle.setAttribute('aria-expanded', String(open));
        if (restoreFocus) menuToggle.focus();
      }
      menuToggle.addEventListener('click', function () {
        setMenu(menuToggle.getAttribute('aria-expanded') !== 'true');
      });
      mainNav.addEventListener('click', function (event) {
        if (event.target.closest('a')) setMenu(false);
      });
      document.addEventListener('keydown', function (event) {
        if (event.key === 'Escape' && mainNav.classList.contains('open')) {
          setMenu(false, true);
        }
      });
      document.addEventListener('click', function (event) {
        if (mainNav.classList.contains('open') && !mainNav.contains(event.target) && !menuToggle.contains(event.target)) {
          setMenu(false);
        }
      });
    }

    var siteData = window.SITE_DATA || {};
    var publications = Array.isArray(siteData.publications) ? siteData.publications : [];
    var publicationMap = new Map(publications.map(function (publication) {
      return [String(publication.id), publication];
    }));
    var list = document.getElementById('publication-list');
    var rows = list ? Array.from(list.querySelectorAll('[data-publication]')) : [];
    var search = document.getElementById('pub-search');
    var year = document.getElementById('pub-year');
    var type = document.getElementById('pub-type');
    var selected = document.getElementById('pub-selected');
    var count = document.getElementById('pub-count');
    var empty = document.getElementById('pub-empty');
    var more = document.getElementById('pub-more');
    var bibButton = document.getElementById('download-bib');
    var csvButton = document.getElementById('download-csv');
    var pageSize = 30;
    var visibleLimit = pageSize;
    var matchingRows = rows.slice();

    function choice(element) {
      if (!element) return '';
      if (element.type === 'checkbox') return element.checked ? 'selected' : '';
      var value = normalize(element.value);
      return value === 'all' ? '' : value;
    }

    function filteredPublications() {
      if (!list) return publications.slice();
      return matchingRows.map(function (row) {
        return publicationMap.get(row.dataset.publication);
      }).filter(Boolean);
    }

    function updatePublications(reset) {
      if (!list) return;
      if (reset) visibleLimit = pageSize;
      var query = normalize(search && search.value);
      var terms = query ? query.split(/\s+/) : [];
      var chosenYear = choice(year);
      var chosenType = choice(type);
      var selectedOnly = choice(selected) === 'selected';
      matchingRows = rows.filter(function (row) {
        var haystack = normalize(row.dataset.search || row.textContent);
        return terms.every(function (term) { return haystack.includes(term); }) &&
          (!chosenYear || normalize(row.dataset.year) === chosenYear) &&
          (!chosenType || normalize(row.dataset.type) === chosenType) &&
          (!selectedOnly || row.dataset.selected === 'true');
      });
      var visibleRows = new Set(matchingRows.slice(0, visibleLimit));
      rows.forEach(function (row) { row.hidden = !visibleRows.has(row); });
      if (count) {
        count.textContent = matchingRows.length === 0 ? 'No publications found' :
          'Showing ' + visibleRows.size + ' of ' + matchingRows.length + ' publication' + (matchingRows.length === 1 ? '' : 's');
      }
      if (empty) empty.hidden = matchingRows.length !== 0;
      if (more) {
        more.hidden = matchingRows.length <= visibleLimit;
        more.textContent = 'Show ' + Math.min(pageSize, Math.max(0, matchingRows.length - visibleLimit)) + ' more';
      }
      [bibButton, csvButton].forEach(function (button) {
        if (!button) return;
        var unavailable = filteredPublications().length === 0;
        button.setAttribute('aria-disabled', String(unavailable));
        if ('disabled' in button) button.disabled = unavailable;
      });
    }

    if (list) {
      if (search) {
        var initialQuery = new URLSearchParams(window.location.search).get('q');
        if (initialQuery !== null) search.value = initialQuery;
      }
      if (count) {
        count.setAttribute('aria-live', 'polite');
        count.setAttribute('aria-atomic', 'true');
      }
      [search, year, type, selected].forEach(function (control) {
        if (!control) return;
        control.addEventListener(control === search ? 'input' : 'change', function () {
          updatePublications(true);
        });
      });
      if (more) {
        more.addEventListener('click', function (event) {
          event.preventDefault();
          var firstNewRow = matchingRows[visibleLimit];
          visibleLimit += pageSize;
          updatePublications(false);
          if (more.hidden && firstNewRow) {
            var nextFocus = firstNewRow.querySelector('a, button');
            if (nextFocus) nextFocus.focus({ preventScroll: true });
          }
        });
      }
      updatePublications(true);
    }

    function authorNames(publication) {
      var names = publication.authors_list;
      if (!Array.isArray(names) && Array.isArray(publication.authors)) names = publication.authors;
      return Array.isArray(names) ? names.map(function (name) {
        if (typeof name === 'string') return text(name);
        if (name && typeof name === 'object') {
          return text(name.name || name.literal || [name.given, name.family].filter(Boolean).join(' '));
        }
        return '';
      }).filter(Boolean) : [];
    }

    function authorsText(publication) {
      var names = authorNames(publication);
      return names.length ? names.join(', ') : text(publication.authors);
    }

    function publicationUrl(publication) {
      return text(publication.doi_url || (publication.doi ? 'https://doi.org/' + publication.doi : '') || publication.url || publication.source_url);
    }

    function citation(publication) {
      var details = publication.bibliographic_details;
      if (!details) {
        details = [
          publication.volume ? String(publication.volume) + (publication.issue ? '(' + publication.issue + ')' : '') : '',
          publication.pages || publication.article_number
        ].filter(Boolean).join(', ');
      }
      return [
        authorsText(publication).replace(/\.$/, ''),
        publication.year ? '(' + publication.year + ')' : '',
        text(publication.title).replace(/\.$/, ''),
        text(publication.venue || publication.journal),
        text(details).replace(/\.$/, '')
      ].filter(Boolean).join('. ') + '. ' + publicationUrl(publication);
    }

    document.addEventListener('click', async function (event) {
      var button = event.target.closest('[data-cite]');
      if (!button) return;
      event.preventDefault();
      var publication = publicationMap.get(button.dataset.cite);
      if (!publication) {
        notify('This citation is not available yet. Please use the paper link.');
        return;
      }
      var value = citation(publication);
      try {
        if (!navigator.clipboard || !navigator.clipboard.writeText) throw new Error('Clipboard unavailable');
        await navigator.clipboard.writeText(value);
        notify('Citation copied.');
      } catch (error) {
        download(value + '\n', 'citation-' + safeKey(publication.id) + '.txt', 'text/plain;charset=utf-8');
        notify('Citation saved as a text file.');
      }
    });

    function safeKey(value) {
      return String(value || 'publication').replace(/[^a-zA-Z0-9_-]/g, '-').slice(0, 100);
    }

    function bibEscape(value) {
      var escapes = {
        '\\': '\\textbackslash{}', '{': '\\{', '}': '\\}', '$': '\\$',
        '&': '\\&', '#': '\\#', '%': '\\%', '_': '\\_',
        '~': '\\textasciitilde{}', '^': '\\textasciicircum{}'
      };
      return text(value).replace(/[\\{}$&#%_~^]/g, function (character) { return escapes[character]; });
    }

    function bibEntry(publication, index) {
      var fields = [];
      function add(key, value, protectCase) {
        if (value == null || value === '') return;
        var escaped = bibEscape(value);
        fields.push('  ' + key + ' = {' + (protectCase ? '{' + escaped + '}' : escaped) + '}');
      }
      add('title', publication.title, true);
      var names = authorNames(publication);
      if (names.length) {
        fields.push('  author = {' + names.map(bibEscape).join(' and ') + '}');
      } else if (text(publication.authors)) {
        // Preserve a supplied author string literally instead of guessing where names end.
        fields.push('  author = {{' + bibEscape(publication.authors) + '}}');
      }
      var conference = publication.type === 'conference';
      var chapter = publication.type === 'book_chapter';
      add(conference || chapter ? 'booktitle' : 'journal', publication.venue || publication.journal);
      add('publisher', publication.publisher);
      add('editor', publication.editor);
      add('year', publication.year);
      add('volume', publication.volume);
      add('number', publication.issue);
      add('pages', publication.pages ? String(publication.pages).replace(/[–—]/g, '--') : '');
      add('eid', publication.article_number);
      add('doi', publication.doi);
      add('url', publicationUrl(publication));
      if (!publication.volume && !publication.pages && !publication.article_number) add('note', publication.bibliographic_details);
      return '@' + (conference ? 'inproceedings' : chapter ? 'incollection' : 'article') + '{' + safeKey(publication.id || 'publication-' + index) + ',\n' + fields.join(',\n') + '\n}';
    }

    function csvCell(value) {
      var cell = String(value == null ? '' : value);
      // Keep spreadsheet software from interpreting citation text as a formula.
      if (/^[\s\uFEFF]*[=+@-]/.test(cell) || /^[\t\r\n]/.test(cell)) cell = "'" + cell;
      return '"' + cell.replace(/"/g, '""') + '"';
    }

    if (bibButton) bibButton.addEventListener('click', function (event) {
      event.preventDefault();
      var filtered = filteredPublications();
      if (!filtered.length) {
        notify('There are no matching publications to download.');
        return;
      }
      download(filtered.map(bibEntry).join('\n\n') + '\n', 'sungjin-choi-publications.bib', 'text/plain;charset=utf-8');
      notify('Prepared ' + filtered.length + ' publication' + (filtered.length === 1 ? '' : 's') + ' for download.');
    });

    if (csvButton) csvButton.addEventListener('click', function (event) {
      event.preventDefault();
      var filtered = filteredPublications();
      if (!filtered.length) {
        notify('There are no matching publications to download.');
        return;
      }
      var table = [['Year', 'Type', 'Title', 'Authors', 'Venue', 'Details', 'DOI', 'URL']];
      filtered.forEach(function (publication) {
        table.push([publication.year, publication.type, publication.title, authorsText(publication),
          publication.venue || publication.journal, publication.bibliographic_details || publication.citation,
          publication.doi, publicationUrl(publication)]);
      });
      var csv = '\uFEFF' + table.map(function (row) { return row.map(csvCell).join(','); }).join('\r\n') + '\r\n';
      download(csv, 'sungjin-choi-publications.csv', 'text/csv;charset=utf-8');
      notify('Prepared ' + filtered.length + ' publication' + (filtered.length === 1 ? '' : 's') + ' for download.');
    });

    var mediaType = document.getElementById('media-type');
    if (mediaType) {
      var mediaRows = Array.from(document.querySelectorAll('[data-media-category]'));
      var mediaCount = document.getElementById('media-count');
      var mediaEmpty = document.getElementById('media-empty');
      function filterMedia() {
        var category = choice(mediaType);
        var visible = 0;
        mediaRows.forEach(function (row) {
          row.hidden = Boolean(category && normalize(row.dataset.mediaCategory) !== category);
          if (!row.hidden) visible += 1;
        });
        if (mediaCount) mediaCount.textContent = visible + ' stor' + (visible === 1 ? 'y' : 'ies');
        if (mediaEmpty) mediaEmpty.hidden = visible !== 0;
      }
      mediaType.addEventListener('change', filterMedia);
      filterMedia();
    }

    var tabs = Array.from(document.querySelectorAll('[data-tab]'));
    var panels = Array.from(document.querySelectorAll('[data-panel]'));
    if (tabs.length && panels.length) {
      function activateTab(name, updateHash) {
        if (!tabs.some(function (tab) { return tab.dataset.tab === name; })) return;
        tabs.forEach(function (tab) {
          var active = tab.dataset.tab === name;
          tab.classList.toggle('active', active);
          tab.setAttribute('aria-selected', String(active));
          tab.tabIndex = active ? 0 : -1;
        });
        panels.forEach(function (panel) { panel.hidden = panel.dataset.panel !== name; });
        if (updateHash) {
          try { window.history.replaceState(null, '', '#' + encodeURIComponent(name)); } catch (error) { /* Local previews may restrict history updates. */ }
        }
      }
      tabs.forEach(function (tab, index) {
        tab.addEventListener('click', function (event) {
          event.preventDefault();
          activateTab(tab.dataset.tab, true);
        });
        tab.addEventListener('keydown', function (event) {
          var next;
          if (event.key === 'ArrowRight' || event.key === 'ArrowDown') next = (index + 1) % tabs.length;
          if (event.key === 'ArrowLeft' || event.key === 'ArrowUp') next = (index - 1 + tabs.length) % tabs.length;
          if (event.key === 'Home') next = 0;
          if (event.key === 'End') next = tabs.length - 1;
          if (next === undefined) return;
          event.preventDefault();
          activateTab(tabs[next].dataset.tab, true);
          tabs[next].focus();
        });
      });
      function readTabHash() {
        var name;
        try { name = decodeURIComponent(window.location.hash.slice(1)); } catch (error) { name = ''; }
        var initial = tabs.find(function (tab) { return tab.dataset.tab === name; }) ||
          tabs.find(function (tab) { return tab.getAttribute('aria-selected') === 'true'; }) || tabs[0];
        activateTab(initial.dataset.tab, false);
      }
      window.addEventListener('hashchange', readTabHash);
      readTabHash();
    }

    var printProfile = document.getElementById('print-profile');
    if (printProfile) printProfile.addEventListener('click', function (event) {
      event.preventDefault();
      window.print();
    });
  }

  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', start, { once: true });
  else start();
})();
