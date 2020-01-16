var drag = dragula([document.getElementById('columns')]);
var selectedField;

/** General functions **/
function parseJSON(string) {
  try {
    return JSON.parse(string)
  } catch (e) {
    return null;
  }
}

function getProviderDefaults(provider) {
  return providers.hasOwnProperty(provider) ?
    Object.values(providers[provider].args).reduce(function (acc, val) {
      return {...acc, [val["name"]]: val["default"]};
    }, {}) : {};
}


/** Data table functions **/
function generateData() {

  var schema = {
    "num_rows": parseInt(document.querySelector('#num_rows').value),
    "include_header": document.querySelector('#include_header').checked,
    "is_nested": document.querySelector('#is_nested').checked,
    "exclude_null": document.querySelector('#exclude_null').checked,
    "columns": []
  };

  var options = ['schema', 'file_format', 'delimiter', 'key_separator', 'quote_character', 'template', 'root_node', 'table_name'];
  options.forEach(function (option) {
    schema[option] = document.querySelector('#' + option).value;
  });

  [].forEach.call(document.querySelectorAll('#columns .form-row'), function (column) {

    var field = {
      "truncate": column.querySelector('input[name="truncate"]').checked,
      "percent_empty": parseInt(column.querySelector('input[name="percent_empty"]').value)
    }
    var fields = ['name', 'type', 'format', 'truncate', 'function'];

    fields.forEach(function (prop) {
      var value = column.querySelector('input[name="' + prop + '"]').value;

      if (value != '') {
        field[prop] = value;
      }

    });

    var args = parseJSON(column.querySelector('input[name="args"]').value);

    if (args) {
      field['args'] = args;
    }

    schema.columns.push(field);

  });

  var request = new XMLHttpRequest();
  request.open('POST', '/api/schema/generate', true);
  request.setRequestHeader("Content-Type", "application/json");

  request.onreadystatechange = function() {
      if (this.readyState === XMLHttpRequest.DONE && this.status === 200) {

          // Create hidden 'a' tag
          var a = document.createElement("a");
          a.style = "display: none;";
          a.href = window.URL.createObjectURL(new Blob([this.response]));

          // Assign file name
          var filename = "mock_data." + document.querySelector('#file_format').value;
          var disposition = this.getResponseHeader('Content-Disposition');
          if (disposition && disposition.indexOf('attachment') !== -1) {
              var filenameRegex = /filename[^;=\n]*=((['"]).*?\2|[^;\n]*)/;
              var matches = filenameRegex.exec(disposition);
              if (matches != null && matches[1]) {
                filename = matches[1].replace(/['"]/g, '');
              }
          }
          a.download = filename;

          // Add 'a' and click
          document.body.appendChild(a);
          a.click();
          a.remove();

      }
  };

  request.send(JSON.stringify(schema));

}

function addColumn() {
  var template = document.getElementById('columnTemplate');
  var node = document.importNode(template.content, true);
  document.getElementById('columns').appendChild(node);
}

function removeColumn(column) {
  $(column.closest('.form-row')).remove();
}

function updateFileFormat() {

  [].forEach.call(document.querySelectorAll('#schemaOptions .optionGroup'), function (optionGroup) {
    optionGroup.style.display = "none";
  });

  switch (document.querySelector('#file_format').value) {
    case 'json':
      document.getElementById('jsonOptions').style.display = 'block';
      break;
    case 'sql':
      document.getElementById('sqlOptions').style.display = 'block';
      break;
    case 'xml':
      document.getElementById('xmlOptions').style.display = 'block';
      break;
    case 'html':
      document.getElementById('templateOptions').style.display = 'block';
      break;
    case 'csv':
    case 'tsv':
    default:
      document.getElementById('csvOptions').style.display = 'block';
      break;
  }

}


/** Data row functions **/
function openModal(button, modalId) {
    selectedField = $(button).closest('.input-group').find('input[name="type"]')[0];
    document.querySelector('#fieldPercentEmpty').value = $(selectedField).siblings('input[name="percent_empty"]')[0].value;
    document.querySelector('#fieldFormat').value = $(selectedField).siblings('input[name="format"]')[0].value;
    document.querySelector('#fieldFunction').value = $(selectedField).siblings('input[name="function"]')[0].value;
    document.querySelector('#fieldTruncate').checked = $(selectedField).siblings('input[name="truncate"]')[0].checked;

    removeAllArguments();
    var args = parseJSON($(selectedField).siblings('input[name="args"]')[0].value);

    var defaults = getProviderDefaults(selectedField.value);
    var allArgs = {...defaults, ...args};

    if (allArgs.constructor === Object && Object.keys(allArgs).length !== 0) {
        Object.keys(allArgs).forEach(function (arg) {
          addArgument(arg, (allArgs[arg] !== null ? JSON.stringify(allArgs[arg]) : null));
        });
    } else {
      addArgument();
    }

    $(modalId).modal({show: true});
}


/** Field type modal functions **/
function chooseFieldType(option) {
  selectedField.value = option;
  $('#fieldTypeModal').modal('hide');
}


/** Field config modal functions **/
function addArgument(name = null, value = null) {
  var template = document.getElementById('argumentTemplate');
  var node = document.importNode(template.content, true);

  if (name) {
    node.querySelector('input[name="argumentName"]').value = name;
    node.querySelector('input[name="argumentValue"]').value = value;
  }

  document.getElementById('arguments').appendChild(node);
}

function removeArgument(argument) {
  $(argument.closest('.form-row')).remove();
}

function removeAllArguments() {
  const arguments = document.getElementById('arguments');
  while (arguments.firstChild) {
    arguments.removeChild(arguments.firstChild);
  }
}

function getArguments() {

  var args = {};

  [].forEach.call(document.querySelectorAll('#arguments .form-row'), function (arg) {
    args[arg.querySelector('input[name="argumentName"]').value] = arg.querySelector('input[name="argumentValue"]').value;
  });

  return Object.keys(args).length !== 0 ? args : null;
}

function saveFieldConfigs() {

  $(selectedField).siblings('input[name="percent_empty"]')[0].value = document.querySelector('#fieldPercentEmpty').value;
  $(selectedField).siblings('input[name="format"]')[0].value = document.querySelector('#fieldFormat').value;
  $(selectedField).siblings('input[name="function"]')[0].value = document.querySelector('#fieldFunction').value;
  $(selectedField).siblings('input[name="truncate"]')[0].checked = document.querySelector('#fieldTruncate').checked;
  $(selectedField).siblings('input[name="args"]')[0].value = JSON.stringify(getArguments());

  $('#fieldConfigModal').modal('hide');
}
