<h1>🌐 Reverse Geocode Automation using Olamaps API</h1>

<p>This project automates the process of reverse geocoding geographical coordinates (latitude and longitude) using the <strong>Olamaps API</strong>. It reads coordinate data from a CSV file, fetches the corresponding address components, and writes the enriched data back to an output CSV file.</p>

<h2>📁 Project Structure</h2>
<pre><code>├── reverseGeocode.py      # Main script for reverse geocoding
├── test_coordinates.csv   # Input CSV file containing Latitude and Longitude
├── output.csv             # Output file generated after processing
</code></pre>

<h2>🚀 Features</h2>
<ul>
  <li>Reads latitude and longitude from a CSV file</li>
  <li>Fetches location details: Country, State, City, Region, Postal Code</li>
  <li>Tracks progress and estimated time of completion</li>
  <li>Periodically saves progress to prevent data loss</li>
  <li>Handles retries and errors gracefully</li>
</ul>

<h2>🧾 Requirements</h2>
<p>Python 3.7+ and the following libraries:</p>
<pre><code>pip install pandas numpy requests</code></pre>

<h2>⚙️ Setup Instructions</h2>
<ol>
  <li>Clone this repository:
    <pre><code>git clone https://github.com/HRI-India/API_Code.git
cd API_Code</code></pre>
  </li>
  <li>Update file paths in <code>reverseGeocode.py</code> if needed:
    <pre><code>input_file = "test_coordinates.csv"
output_file = "output.csv"</code></pre>
  </li>
  <li>Run the script:
    <pre><code>python reverseGeocode.py</code></pre>
  </li>
</ol>

<h2>📥 Input File Format (<code>test_coordinates.csv</code>)</h2>
<table>
  <tr><th>Latitude</th><th>Longitude</th></tr>
  <tr><td>12.9716</td><td>77.5946</td></tr>
  <tr><td>...</td><td>...</td></tr>
</table>

<h2>📤 Output File Format (<code>output.csv</code>)</h2>
<table>
  <tr>
    <th>Latitude</th>
    <th>Longitude</th>
    <th>Country</th>
    <th>State</th>
    <th>City</th>
    <th>Region</th>
    <th>Postal Code</th>
    <th>Formatted Address</th>
  </tr>
  <tr>
    <td>...</td>
    <td>...</td>
    <td>...</td>
    <td>...</td>
    <td>...</td>
    <td>...</td>
    <td>...</td>
    <td>...</td>
  </tr>
</table>

<h2>🔐 API Key</h2>
<p>Make sure your <code>api_key</code> for Olamaps is valid. You can replace it inside the script:</p>
<pre><code>api_key = 'YOUR_API_KEY_HERE'</code></pre>

<h2>🛠 Customization</h2>
<p>To rename address columns in the output:</p>
<pre><code>input_df.rename(columns={
    "country": "Country",
    "administrative_area_level_1": "State",
    "administrative_area_level_2": "City",
    "administrative_area_level_3": "Region"
}, inplace=True)</code></pre>

<h2>🧪 Example Usage</h2>
<pre><code>python reverseGeocode.py</code></pre>
<p>Console output will show progress:</p>
<pre><code>Processing row 5/200 | 2.50% complete | ETA: 4m 32s | Elapsed: 0m 37s</code></pre>