# Circuit Designer

A sophisticated power electronics circuit design tool built with Streamlit that helps engineers and designers select optimal components for their circuits.

## 🚀 Features

### 1. Circuit Design Support
- **PFC (Power Factor Correction) Circuit Design**
  - Input voltage range: 100V-240V
  - Output voltage range: 380V-400V
  - Power ratings up to 3000W
  - Automatic component value calculation
  - Efficiency optimization

- **Buck Converter Design**
  - Input voltage range: 12V-24V
  - Output voltage range: 3.3V-5V
  - Power ratings up to 50W
  - Comprehensive ripple and transient analysis

### 2. Intelligent Component Selection
- **MOSFET Selection**
  - Database of cutting-edge MOSFETs
  - Automatic filtering based on:
    - Voltage ratings
    - Current capabilities
    - Package types
    - Efficiency ranges
  - Smart recommendations considering:
    - RDS(on)
    - Gate charge
    - Thermal characteristics

- **Capacitor Selection**
  - Extensive capacitor database including:
    - MLCCs
    - Polymer Aluminum
    - Electrolytic capacitors
  - Selection criteria:
    - Capacitance values
    - Voltage ratings
    - ESR specifications
    - Temperature ranges
    - Life expectancy

- **Inductor Selection**
  - Comprehensive inductor database
  - Selection based on:
    - Inductance values
    - Current ratings
    - DC resistance
    - Core types
    - Package specifications

### 3. Interactive Component Library
- **Visual Database Explorer**
  - Browse complete component databases
  - Filter and sort capabilities
  - Highlighted performance metrics
  - Comparative analysis tools

### 4. User Interface Features
- **Clean, Modern Design**
  - Intuitive navigation
  - Responsive layout
  - Professional styling
  - Clear component visualization

- **Real-time Calculations**
  - Instant feedback on parameter changes
  - Automatic validation of inputs
  - Error handling and user guidance

## 🛠️ Technical Specifications

### Technology Stack
- **Frontend:** Streamlit
- **Backend:** Python
- **Data Processing:** Pandas
- **Component Database:** CSV-based data storage

### Key Dependencies
- streamlit
- pandas
- numpy

### Data Management
- Efficient data processing
- Optimized component filtering
- Smart caching for performance

## 📊 Component Databases

### MOSFET Database
- Industry-standard components
- Performance characteristics
- Application recommendations
- Efficiency ratings
- Package specifications
- Manufacturer details

### Capacitor Database
- Multiple capacitor types
- Detailed specifications
- Application notes
- Performance metrics
- Physical dimensions
- Reliability data

### Inductor Database
- Common power inductors
- Current ratings
- Core specifications
- Package details
- Performance metrics

## 🎯 Use Cases

1. **Power Supply Design**
   - PFC stage design
   - DC-DC converter optimization
   - Component selection for specific requirements

2. **Industrial Applications**
   - Motor drive circuits
   - Power conversion systems
   - High-efficiency designs

3. **Consumer Electronics**
   - Voltage regulators
   - Battery charging circuits
   - LED drivers

## 🚀 Getting Started

1. **Installation**
   ```bash
   git clone https://github.com/rishabh-iitbhu/Circuit-Designer.git
   cd circuit_designer
   pip install -r requirements.txt
   ```

2. **Running the Application**
   ```bash
   streamlit run app.py
   ```

## 🔧 Usage

1. Select the circuit type (PFC or Buck Converter)
2. Enter your design requirements
3. Click "Calculate Component Values"
4. Review the suggested components
5. Access the component library for detailed information

## 📝 Notes

- All calculations include appropriate safety margins
- Component suggestions consider real-world availability
- Database is updated with latest components (as of October 2025)
- Recommendations prioritize efficiency and reliability

## 👥 Target Users

- Power Electronics Engineers
- Circuit Designers
- Electronics Hobbyists
- Students and Researchers

## 🔜 Future Enhancements

- Additional circuit topologies
- Advanced thermal analysis
- Cost optimization features
- PCB layout recommendations
- Integration with supplier APIs

## 📫 Contact

For questions and feedback, please open an issue on GitHub.