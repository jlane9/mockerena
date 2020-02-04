const drag = dragula([document.getElementById('columns')]);
let selectedColumn;

/* === General functions === */

/**
 * Safely parses JSON string
 *
 * @param {string} string - JSON string
 * @returns {null|Object} - JSON object parsed from string
 */
function parseJSON(string) {
  try {
    return JSON.parse(string)
  } catch (e) {
    return null;
  }
}

/**
 * Returns provider type default arguments
 *
 * @param {string} provider - Provider type key
 * @returns {Object} - Provider type argument defaults
 */
function getProviderDefaults(provider) {
  return providers.hasOwnProperty(provider) ? Object.values(providers[provider].args).reduce((acc, val) => {
      return Object.assign(acc, {[val["name"]]: val["default"]});
  }, {}) : {};
}


/* === Data table functions  === */

/**
 * Add column to schema
 */
function addColumn() {
  const template = document.getElementById('columnTemplate');
  let node = document.importNode(template.content, true);
  let columns = document.getElementById('columns');

  // Use the same column type of the last column
  node.querySelector('input[name="type"]').value = columns.lastElementChild.querySelector('input[name="type"]').value;

  columns.appendChild(node);
}

/**
 * Checks whether schema is valid
 *
 * @returns {boolean} - True if the schema is valid, false otherwise
 */
function isValidSchema() {

    let columns, element, valid;

    const properties = ["schema", "num_rows", "template"];
    valid = true;
    columns = document.querySelectorAll('input[name="name"]');


    for (const property of properties) {

        element = document.querySelector("#" + property);

        if (element.checkValidity()) {
            element.classList.remove("is-invalid");
        } else {
            element.classList.add("is-invalid");
            valid = false;
        }

    }

    for (const column of columns) {
        if (column.checkValidity()) {
            column.classList.remove("is-invalid");
        } else {
            column.classList.add("is-invalid");
            valid = false;
        }
    }

    return valid;
}

/**
 * Remove column from schema
 *
 * @param {HTMLElement} column - Column to remove
 */
function removeColumn(column) {
  $(column.closest('.form-row')).remove();
}

/**
 * Update file format option
 */
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


/* === Data row functions  === */

/**
 *
 * @param {HTMLElement} button
 * @param {string}  modalId
 */
function openModal(button, modalId) {
    selectedColumn = $(button).closest('.input-group').find('input[name="type"]')[0];

    const columnFormat = $(selectedColumn).siblings('input[name="format"]')[0].value;
    const columnPercentEmpty = $(selectedColumn).siblings('input[name="percent_empty"]')[0].value;
    const columnFunction = $(selectedColumn).siblings('input[name="function"]')[0].value;
    const columnTruncate = $(selectedColumn).siblings('input[name="truncate"]')[0].checked;

    document.querySelector('#fieldPercentEmpty').value = columnPercentEmpty ? columnPercentEmpty : 0;
    document.querySelector('#fieldFormat').value = columnFormat ? columnFormat : "%Y-%m-%d %H:%M:%S";
    document.querySelector('#fieldFunction').value = columnFunction;
    document.querySelector('#fieldTruncate').checked = columnTruncate;

    removeAllArguments();
    let args = parseJSON($(selectedColumn).siblings('input[name="args"]')[0].value);

    let defaults = getProviderDefaults(selectedColumn.value);
    let allArgs = {...defaults, ...args};

    if (allArgs.constructor === Object && Object.keys(allArgs).length !== 0) {
        Object.keys(allArgs).forEach(function (arg) {
          addArgument(arg, (allArgs[arg] !== null ? JSON.stringify(allArgs[arg]) : null));
        });
        document.getElementById("argumentGroup").style.display = "";
    } else {
      document.getElementById("argumentGroup").style.display = "none";
    }

    switch (modalId) {
      case "#fieldTypeModal":
        clearColumnTypeSearch();
        break;
      case "#fieldConfigModal":
        isValidColumnConfig();
        break;
      default:
        break;
    }

    $(modalId).modal({show: true});
}


/* === Field type modal functions === */

/**
 * Update selected column provider type and close modal
 *
 * @param {string} providerType - Provider type name
 */
function chooseFieldType(providerType) {
  selectedColumn.value = providerType;
  $('#fieldTypeModal').modal('hide');
}

/**
 * Filter provider types
 */
function filterProviderType() {

  let providers, subtitle, title;
  const category = document.getElementById("toggleColumnTypeCategory").innerText.toUpperCase();
  const search = document.getElementById("columnTypeSearch").value.toUpperCase();
  providers = document.querySelectorAll(".providers .provider");

  for (const provider of providers) {
    title = provider.querySelector(".card-title").innerText.toUpperCase();
    subtitle = provider.querySelector(".card-subtitle").innerText.toUpperCase();
    subtitle = subtitle ? subtitle : "BASIC";
    provider.style.display = title.indexOf(search) > -1 && (subtitle.indexOf(category) > -1 || category === "ALL") ? "" : "none";
  }

}

/**
 * Update and filter provider type category
 *
 * @param {HTMLElement} category - Category selection
 */
function updateProviderTypeCategory(category) {
  document.getElementById("toggleColumnTypeCategory").innerText = category.innerText;
  filterProviderType();
}

/**
 * Clear column type search
 */
function clearColumnTypeSearch() {

  let providers = document.querySelectorAll(".providers .provider");

  for (const provider of providers) {
    provider.style.display = "";
  }

  document.getElementById("columnTypeSearch").value = "";
  document.getElementById("toggleColumnTypeCategory").innerText = "All";

}


/* === Column configuration modal functions === */

/**
 * Add argument to column configuration modal, with optional value
 *
 * @param {?string} name - Argument name (optional)
 * @param {?string} value - Argument value (optional)
 */
function addArgument(name = null, value = null) {

  let template = document.getElementById('argumentTemplate');
  let node = document.importNode(template.content, true);

  if (name) {
    node.querySelector('input[name="argumentName"]').value = name;
    node.querySelector('input[name="argumentValue"]').value = value;
  }

  document.getElementById('arguments').appendChild(node);

}

/**
 * Retrieve all column arguments
 *
 * @returns {object} - Map of column arguments
 */
function getArguments() {

  let args = {};

  [].forEach.call(document.querySelectorAll('#arguments .form-row'), function (arg) {
    args[arg.querySelector('input[name="argumentName"]').value] = arg.querySelector('input[name="argumentValue"]').value;
  });

  function filterEmpty(key) {
    return key !== "" && args[key] !== "" && args[key] !== null;
  }

  function createMap(map, key) {
    return map.concat({[key]: args[key]});
  }

  return Object.keys(args).length !== 0 ? Object.keys(args).filter(filterEmpty).reduce(createMap, {}) : null;
}

/**
 * Checks whether all columns configurations are valid
 *
 * @returns {boolean} - True, if all configurations for column are valid
 */
function isValidColumnConfig() {

  let element, columnFunction, valid;
  const columns = ["fieldConfig", "fieldPercentEmpty", "fieldFormat"];

  valid = true;
  columnFunction = document.querySelector("#fieldFunction");


  for (const column of columns) {

    element = document.querySelector("#" + column);

    if (element.checkValidity()) {
      element.classList.remove("is-invalid");
    } else {
      element.classList.add("is-invalid");
      valid = false;
    }

  }

  if (validateFunction(columnFunction.value)) {
    columnFunction.classList.remove("is-invalid")
  } else {
    columnFunction.classList.add("is-invalid");
    valid = false;
  }

  return valid;
}

/**
 * Remove all arguments from column configuration modal
 */
function removeAllArguments() {
  const arguments = document.getElementById('arguments');
  while (arguments.firstChild) {
    arguments.removeChild(arguments.firstChild);
  }
}

/**
 * Saves column configuration and closes modal
 */
function saveColumnConfigs() {

  if (!isValidColumnConfig()) {
    return;  // Keep modal open if configuration is invalid
  }

  $(selectedColumn).siblings('input[name="percent_empty"]')[0].value = document.querySelector('#fieldPercentEmpty').value;
  $(selectedColumn).siblings('input[name="format"]')[0].value = document.querySelector('#fieldFormat').value;
  $(selectedColumn).siblings('input[name="function"]')[0].value = document.querySelector('#fieldFunction').value;
  $(selectedColumn).siblings('input[name="truncate"]')[0].checked = document.querySelector('#fieldTruncate').checked;
  $(selectedColumn).siblings('input[name="args"]')[0].value = JSON.stringify(getArguments());

  $('#fieldConfigModal').modal('hide');

}


/* === Rest services === */

/**
 * Generate data from schema
 */
function generateData() {

    if (!isValidSchema()) {
        return; // Do not generate data if schema is invalid
    }

  let schema = {
    "num_rows": parseInt(document.querySelector('#num_rows').value),
    "include_header": document.querySelector('#include_header').checked,
    "is_nested": document.querySelector('#is_nested').checked,
    "exclude_null": document.querySelector('#exclude_null').checked,
    "columns": []
  };

  const options = ['schema', 'file_format', 'delimiter', 'key_separator', 'quote_character', 'template', 'root_node', 'table_name'];

  for (option of options) {
    schema[option] = document.querySelector('#' + option).value;
  }

  [].forEach.call(document.querySelectorAll('#columns .form-row'), function (column) {

    let field = {
      "truncate": column.querySelector('input[name="truncate"]').checked,
      "percent_empty": parseInt(column.querySelector('input[name="percent_empty"]').value)
    };
    let fields = ['name', 'type', 'format', 'truncate', 'function'];

    fields.forEach(function (prop) {
      let value = column.querySelector('input[name="' + prop + '"]').value;

      if (value !== '') {
        field[prop] = value;
      }

    });

    let args = parseJSON(column.querySelector('input[name="args"]').value);

    if (args) {
      field['args'] = args;
    }

    schema.columns.push(field);

  });

  let request = new XMLHttpRequest();
  request.open('POST', '/api/schema/generate', true);
  request.setRequestHeader("Content-Type", "application/json");

  request.onreadystatechange = function() {
      if (this.readyState === XMLHttpRequest.DONE && this.status === 200) {

          // Create hidden 'a' tag
          let a = document.createElement("a");
          a.style.display = "none";
          a.href = window.URL.createObjectURL(new Blob([this.response]));

          // Assign file name
          let filename = "mock_data." + document.querySelector('#file_format').value;
          let disposition = this.getResponseHeader('Content-Disposition');
          if (disposition && disposition.indexOf('attachment') !== -1) {
              let filenameRegex = /filename[^;=\n]*=((['"]).*?\2|[^;\n]*)/;
              let matches = filenameRegex.exec(disposition);
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

/**
 * Call mockerena to verify function string validity
 *
 * @param {string} func - Function string
 * @returns {boolean} - True if function is valid, false otherwise
 */
function validateFunction(func) {

  let request = new XMLHttpRequest();

  request.open('POST', '/api/validate-function', false);
  request.send(func);

  return request.readyState === XMLHttpRequest.DONE && request.status === 200 && request.response === "true";

}
