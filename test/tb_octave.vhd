library vunit_lib;
context vunit_lib.vunit_context;
use vunit_lib.integer_array_pkg.all;

entity tb_octave is
  generic (
    runner_cfg       : string;
    num_of_data_sets : natural;
    size_of_data_set : natural;
    activate_bug     : boolean);
end entity tb_octave;

architecture test of tb_octave is
  constant data             : integer_array_t := new_1d(1);
  constant processing_delay : natural         := 20000000;

  impure function get_output_sample return integer is
    variable ret_val : integer;
  begin
    for i in 1 to processing_delay loop
      null;
    end loop;

    ret_val := get(data, 0);
    if activate_bug and get(data, 0) = 87 then
      set(data, 0, get(data, 0) - 30);
    else
      set(data, 0, get(data, 0) + 1);
    end if;

    return ret_val;
  end function;
begin

  test_runner : process is
    variable data_set : integer_array_t;
  begin
    test_runner_setup(runner, runner_cfg);

    for set in 1 to num_of_data_sets loop
      data_set := new_1d;

      for data in 1 to size_of_data_set loop
        append(data_set, get_output_sample);
      end loop;

      save_csv(data_set, file_name => join(output_path(runner_cfg), "data_set_" & to_string(set) & ".csv"));
      deallocate(data_set);
    end loop;

    test_runner_cleanup(runner);

  end process;

end architecture test;
