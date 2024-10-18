FROM debian:latest AS puppy

# prep
RUN apt-get update \
    && apt-get install -y curl \
    && apt-get clean
RUN useradd -m -u 1000 user
USER user

ENV PATH=/home/user/.pixi/bin:$PATH
RUN mkdir $HOME/puppy
WORKDIR $HOME/puppy

# install puppy
RUN curl -fsSL https://raw.githubusercontent.com/liquidcarbon/puppy/main/pup.sh | bash -s 3.12
RUN pup
RUN pixi add marimo
RUN pup add env_plots matplotlib
RUN pup add env_sql altair duckdb pandas plotly polars pyarrow
RUN pup list
RUN cp -r ./.pixi/envs/default/lib/python3.12/site-packages/marimo/_tutorials . && mv _tutorials marimo_tutorials

EXPOSE 7860

CMD ["pixi", "run", "marimo", "tutorial", "sql", "--host", "0.0.0.0", "--port", "7860", "--no-token"]

# deploy without installing
# CMD ["pixi", "run", "uvx", "marimo", "tutorial", "intro", "--host", "0.0.0.0", "--port", "7860", "--no-token"]
