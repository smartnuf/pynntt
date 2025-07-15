# Pynntt - Python Native Network Theory Tools

The project offers tools useful in studying network theory. We build from a core that is a two-pole transformerless network (on-port, two-terminal RLC-network) descriptor language. We provide tools to read and write these descriptors, enumerate them, and analyse analyse and classify both their functional (driving point immittance, regularity, essential regularity f.e.) and structural properties (Simple Series Parallel (SSP), f.e.).

We define our structural descriptor grammar with a view it evaloving over time to include descriptors for three-poles and four-poles, as well as related functional descriptors for two-ports and n-ports, and structureal interconnects to compose then into larger structurs, and decompose into different forms.

## Contributing

### 🚀 Getting Started with Development 
To set up your local development environment :  
1. Clone the repository: <code>git clone https://github.com/smartnuf/pynntt.git</code> 
2. Create a virtual environment (Windows): <code>python -m venv .venv</code> 
3. Activate the virtual environment: <code>.venv\Scripts\Activate.ps1</code> > _If this is blocked by execution policy, run:_ > <code>Set-ExecutionPolicy RemoteSigned -Scope CurrentUser</code> 
4. Install required packages: <code>pip install -r requirements.txt</code> 
5. Run tests: <code>pytest tests/</code> 6. Run the main module (optional): <code>python src/pynntt/networks.py</code> For advanced tasks, refer to docs in the `/doc` folder.
